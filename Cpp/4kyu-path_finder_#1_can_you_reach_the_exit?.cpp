#include <algorithm>
#include <array>
#include <cmath>
#include <iostream>
#include <string>
#include <unordered_set>
#include <vector>

using namespace std;

const int OBSTACLE_WEIGHT = 10000;

class Node {
 public:
  int pos_x, pos_y;
  int g;     // g(n) = g(n-1) + c(n-1, n)
  double f;  // f(n) = g(n) + h(n)
  bool obstacle;
  array<Node *, 4> neighbors{};  // 0-up 1-right 2-down 3-left
  Node *parent;

  Node(){};

  Node(int pos_x, int pos_y, bool obstacle, double h, int g = 0,
       Node *t_parent = nullptr)
      : pos_x(pos_x),
        pos_y(pos_y),
        g(g),
        obstacle(obstacle),
        parent(t_parent),
        h_(h) {
    f = h_ + g + (OBSTACLE_WEIGHT * obstacle);
  };

  Node(Node *ptr) : parent(ptr){};

  void add_neighbor(int direction, int pos_x, int pos_y, bool obstacle,
                    double h, double c = 1.0) {
    Node *neighbor_ = new Node(pos_x, pos_y, obstacle, h, g + c, this);
    neighbors[direction] = neighbor_;
  }

  bool operator==(const Node &node2) {
    return ((this->pos_x == node2.pos_x) && (this->pos_y == node2.pos_y));
  }

 private:
  double h_;
};

class Graph {
 public:
  string maze;
  string path_drawn;
  int goal_x, goal_y;

  Graph(string maze, int goal_x, int goal_y, int posX, int posY, int g = 0)
      : maze(maze), goal_x(goal_x), goal_y(goal_y) {
    root_ = Node(posX, posY, false, heuristic(posX, posY), g);
    max_y_ = count(maze.cbegin(), maze.cend(), '\n') + 1;
    max_x_ = maze.find_first_of("\n");
  };

  Graph(string maze, int g = 0) : maze(maze) {
    max_y_ = count(maze.cbegin(), maze.cend(), '\n') + 1;
    max_x_ = maze.find_first_of("\n");
    goal_x = max_x_ - 1;
    goal_y = max_y_ - 1;
    root_ = Node(0, 0, false, heuristic(0, 0), g);
  };

  double heuristic(int posX, int posY) {
    return sqrt(pow(posX - goal_x, 2) + pow(posY - goal_y, 2));
  }

  bool in_grid(int x, int y) {
    bool x_in_grid = (x >= 0) && (x < max_x_);
    bool y_in_grid = (y >= 0) && (y < max_y_);
    return x_in_grid && y_in_grid;
  }

  bool is_obstacle(int x, int y) {
    int idx = map_coordinate_to_index(x, y);
    return maze[idx] == 'W';
  }

  int map_coordinate_to_index(int x, int y) { return x + ((max_y_ + 1) * y); }

  void print_path() {
    if (!path_drawn.empty()) {
      cout << path_drawn << endl;
    } else if (!path_.empty()) {
      path_drawn = maze;
      for (int step : path_) {
        path_drawn[step] = '*';
      }
      print_path();
    } else {
      cout << "Unreachable" << endl;
    }
  }

  int number_of_steps() { return path_.size(); }

  bool Astar(bool print_priority_queue = false);

 private:
  int max_x_, max_y_;
  Node root_;
  vector<Node *> priority_queue_;
  unordered_set<int> visited_indexes_;
  vector<int> path_;

  void generate_path_(Node *node) {
    vector<int> path;
    while (node->parent != nullptr) {
      path.push_back(map_coordinate_to_index(node->pos_x, node->pos_y));
      node = node->parent;
    }
    path_ = path;
  }

  int node_in_priority_queue_(int x, int y) {
    // Checks if node at (x, y) is already in the priority queue. Returns its
    // index or -1 if node is not in the queue
    for (auto it = priority_queue_.begin(); it != priority_queue_.end(); ++it) {
      if (((*it)->pos_x == x) && ((*it)->pos_y == y)) {
        int index = distance(priority_queue_.begin(), it);
        return index;
      }
    }
    return -1;
  }
};

bool Graph::Astar(bool print_priority_queue) {
  // Based on Howie Choset, K. M. Lynch, and S. Hutchinson, Principles of robot
  // motion: theory, algorithms, and implementations. Cambridge, Mass. Bradford,
  // 2005
  priority_queue_.push_back(&root_);
  bool reached = false;

  while (!priority_queue_.empty()) {
    Node *curr = priority_queue_.back();
    priority_queue_.pop_back();
    if (curr->obstacle) {
      return false;
    }
    int curr_idx = map_coordinate_to_index(curr->pos_x, curr->pos_y);

    if (curr->pos_x == goal_x && curr->pos_y == goal_y) {
      reached = true;
      // Check if exists a possibly cheaper way to reach the goal
      vector<Node *> filtered(priority_queue_.size());
      auto it = copy_if(priority_queue_.begin(), priority_queue_.end(),
                        filtered.begin(),
                        [&](Node *node) { return node->f < curr->g; });
      filtered.resize(distance(filtered.begin(), it));
      priority_queue_ = filtered;

    } else if (visited_indexes_.find(curr_idx) == visited_indexes_.end()) {
      // Node was not visited
      visited_indexes_.insert(curr_idx);
      for (int i = 0; i < 4; i++) {
        int delta_x = (i % 2) * pow(-1, !(i % 3));
        int delta_y = !(i % 2) * pow(-1, !(i % 3));
        int next_x = curr->pos_x + delta_x;
        int next_y = curr->pos_y + delta_y;

        if (in_grid(next_x, next_y)) {
          if (visited_indexes_.find(map_coordinate_to_index(next_x, next_y)) ==
              visited_indexes_.end()) {
            bool obstacle = is_obstacle(next_x, next_y);
            double h = heuristic(next_x, next_y);
            int queue_idx = node_in_priority_queue_(next_x, next_y);
            if (queue_idx == -1) {
              // Node is not on priority queue
              curr->add_neighbor(i, next_x, next_y, obstacle, h);
              priority_queue_.push_back(curr->neighbors[i]);
            } else if (curr->g + 1 < priority_queue_[queue_idx]->g) {
              // Cheaper path to the same node
              priority_queue_.erase(priority_queue_.begin() + queue_idx);
              curr->add_neighbor(i, next_x, next_y, obstacle, h);
              priority_queue_.push_back(curr->neighbors[i]);
            }
          }
        }
      }
      // sorts descending because of pop
      sort(priority_queue_.begin(), priority_queue_.end(),
           [&](Node *node1, Node *node2) { return node1->f > node2->f; });
    }
    if (print_priority_queue) {
      cout << "Priority queue:" << endl;
      for (auto itt : priority_queue_) {
        cout << "(" << itt->pos_x << ", " << itt->pos_y << ")" << endl;
      }
    }
    if (priority_queue_.empty()) {
      if (reached) {
        generate_path_(curr);
      }
    }
  }
  return reached;
}

bool path_finder(string maze) {
  Graph graph(maze);
  bool reachable = graph.Astar();
  return reachable;
}

// TESTING
int main() {
  string maze = "......\n......\n......\n......\n.....W\n....W.";
  maze = ".W...W...W...\n.W.W.W.W.W.W.\n.W.W.W.W.W.W.\n.W.W.W.W.W.W.\n.W.W.W.W.W.W.\n.W.W.W.W.W.W.\n.W.W.W.W.W.W.\n.W.W.W.W.W.W.\n.W.W.W.W.W.W.\n.W.W.W.W.W.W.\n.W.W.W.W.W.W.\n.W.W.W.W.W.W.\n...W...W...W.";
  maze = ".............\nWWWWWWWWWWWW.\n.............\n.WWWWWWWWWWWW\n.............\nWWWWWWWWWWWW.\n.............\n.WWWWWWWWWWWW\n.............\nWWWWWWWWWWWW.\n.............\n.WWWWWWWWWWWW\n.............";
  maze = "....W.W..\n...W.WWWW\n.W...W...\n.W......W\nW.......W\n.WW..WW..\n.W..WW...\n..W....WW\nW.W......";
  cout << maze << endl;
  Graph grafo(maze);
  cout << endl << "==============\nOptimal path:\n==============" << endl;
  bool reached = grafo.Astar();
  grafo.print_path();
  cout << grafo.number_of_steps() << " steps." << endl;
  return 0;
}