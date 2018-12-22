#include <cstdlib>
#include <vector>
#include <ctime>
#include <queue>
#include <iostream>
#include <algorithm>

using namespace std;

struct Job_t
{
    int id;
    int host_id; 
    int start = 0;
    int end = 0;
};

struct Core_t
{
    int id; 
    vector<Job_t *> timetable;
};

struct Parameter_t
{
    int from = 0; 
    int destination = 0; 
    float isolation = 0;
    int idel_time = 0;
    int weight = 0; 
    int container = 0; 
};

void InitializeJob(Job_t* job, int id_in, int host_in, int start_in, int end_in)
{
    job->id = id_in; 
    job->host_id = host_in; 
    job->start = start_in;
    job->end = end_in; 
}

void InitializeSchedule(vector<Core_t *> &schedule)
{
    Core_t* a = new Core_t; 
    Core_t* b = new Core_t; 
    Core_t* c = new Core_t;
    Job_t* job1 = new Job_t;
    Job_t* job2 = new Job_t;
    Job_t* job3 = new Job_t;
    Job_t* job4 = new Job_t;
    Job_t* job5 = new Job_t;
    Job_t* job6 = new Job_t;
    Job_t* job7 = new Job_t;
    Job_t* job8 = new Job_t;
    Job_t* job9 = new Job_t;
    Job_t* job10 = new Job_t;
    InitializeJob(job1, 1, 3, 0, 9);
    InitializeJob(job2, 2, 1, 9, 22);
    InitializeJob(job3, 3, 2, 17, 30);
    InitializeJob(job4, 4, 2, 9, 17);
    InitializeJob(job5, 5, 3, 9, 19); 
    InitializeJob(job6, 6, 3, 19, 28); 
    InitializeJob(job7, 7, 3, 30, 41); 
    InitializeJob(job8, 8, 2, 30, 41);
    InitializeJob(job9, 9, 1, 22, 40);
    InitializeJob(job10, 10, 2, 41, 48); 
    a->id = 1; 
    a->timetable.emplace_back(job2);
    a->timetable.emplace_back(job9);
    b->id = 2; 
    b->timetable.emplace_back(job4);
    b->timetable.emplace_back(job3);
    b->timetable.emplace_back(job8);
    b->timetable.emplace_back(job10);
    c->id = 3;
    c->timetable.emplace_back(job1);
    c->timetable.emplace_back(job5);
    c->timetable.emplace_back(job6);
    c->timetable.emplace_back(job7); 

    schedule.emplace_back(a);
    schedule.emplace_back(b);
    schedule.emplace_back(c);
}

class Graph_t
{
public: 
    int vertex_num = 10;
    vector<vector<Parameter_t> > graph; 

    void InitializeGraph(); 
    void GraphSize(int vertex);
    void GraphIn(int start, int end, int weight); 
};

void Graph_t::InitializeGraph()
{
    for (int i = 0; i < graph.size(); i ++)
    {
        for (int j = 0; j < graph[i].size(); j ++)
        {
            graph[i][j].weight = -1; 
        } 
    }
}

void Graph_t::GraphSize(int vertex)
{
    vertex_num = vertex;
    graph.resize(vertex);
    for (int i = 0; i < graph.size(); i ++)
    {
        graph[i].resize(vertex); 
    }
}

void Graph_t::GraphIn(int start, int end, int weight)
{
    graph[start - 1][end - 1].weight = weight; 
    graph[start - 1][end - 1].from = start; 
    graph[start - 1][end - 1].destination = end; 
}

void VertexInGraph(Graph_t &graph)
{
    graph.GraphIn(1, 2, 18);
    graph.GraphIn(1, 3, 12); 
    graph.GraphIn(1, 4, 9); 
    graph.GraphIn(1, 5, 11);
    graph.GraphIn(1, 6, 14);
    graph.GraphIn(2, 8, 19);
    graph.GraphIn(2, 9, 16);
    graph.GraphIn(3, 7, 23); 
    graph.GraphIn(4, 8, 27); 
    graph.GraphIn(4, 9, 23);
    graph.GraphIn(5, 9, 13);
    graph.GraphIn(6, 8, 15);
    graph.GraphIn(7, 10, 17);
    graph.GraphIn(8, 10, 11); 
    graph.GraphIn(9, 10, 13); 
}

void InitializeIso(Graph_t &graph)
{
    for (int i = 0; i < graph.vertex_num; i ++)
    {
        for (int j = 0; j < graph.vertex_num; j ++)
        {
            if (i <= j)
                graph.graph[i][j].isolation = (rand() % 100) * 0.01; 
            else 
                graph.graph[i][j].isolation = 0; 
        }
    }
}

Job_t* SearchJob(vector<Core_t *> &schedule, int id)
{
    Job_t* result = nullptr; 
    bool found = false; 
    for (int i = 0; i < schedule.size(); i ++)
    {
        auto current_core = schedule[i]; 
        for (int j = 0; j < current_core->timetable.size(); j ++)
        {
            if (current_core->timetable[j]->id == id)
            {
                result = current_core->timetable[j];
                found = true; 
                break; 
            }
        }
        if (found)
            break; 
    }
    return result; 
}

void InitializeIdel(Graph_t &graph, vector<Core_t *> &schedule)
{
    for (int j = graph.vertex_num - 1; j > 0; j --)
    {
        Job_t* current_job = SearchJob(schedule, j + 1); 
        for (int i = 0; i < graph.vertex_num; i ++)
        {
            if (graph.graph[i][j].weight != -1)
            {
                Job_t* pre_job = SearchJob(schedule, i + 1); 
                graph.graph[i][j].idel_time = -1 * (pre_job->end - current_job->start); 
            }
        }
    }
}

void PrintGraph(Graph_t &graph)
{
    cout << "weight: " << endl; 
    for (int i = 0; i < graph.vertex_num; i ++)
    {
        for (int j = 0; j < graph.vertex_num; j ++)
        {
            cout << graph.graph[i][j].weight << " ";
        }
        cout << endl; 
    }
    cout << "isolation: " << endl; 
    for (int i = 0; i < graph.vertex_num; i ++)
    {
        for (int j = 0; j < graph.vertex_num; j ++)
        {
            cout << graph.graph[i][j].isolation << " ";
        }
        cout << endl; 
    }
    cout << "idel_time: " << endl; 
    for (int i = 0; i < graph.vertex_num; i ++)
    {
        for (int j = 0; j < graph.vertex_num; j ++)
        {
            cout << graph.graph[i][j].idel_time << " ";
        }
        cout << endl; 
    }
    cout << "destination: " << endl; 
    for (int i = 0; i < graph.vertex_num; i ++)
    {
        for (int j = 0; j < graph.vertex_num; j ++)
        { 
            cout << graph.graph[i][j].destination << " ";
        }
        cout << endl; 
    }
}

struct compare_edge
{
    bool operator()(Parameter_t a, Parameter_t b) const
    {
        float ratio_a = (float)a.idel_time / (float)a.weight;
        float ratio_b = (float)b.idel_time / (float)b.weight;
        if(ratio_a == ratio_b) 
            return (a.destination > b.destination);
        else 
            return (ratio_a < ratio_b); 
    }
};

void BFS_reverse(Graph_t &graph)
{
    Graph_t reverse; 
    reverse.GraphSize(graph.vertex_num);
    for (int i = 0; i < graph.vertex_num; i ++)
    {
        for (int j = 0; j < graph.vertex_num; j ++)
        {
            int size = graph.vertex_num - 1; 
            reverse.graph[i][j].weight = graph.graph[size - j][size  - i].weight; 
            reverse.graph[i][j].isolation = graph.graph[size - j][size - i].isolation; 
            reverse.graph[i][j].idel_time = graph.graph[size - j][size - i].idel_time; 
            reverse.graph[i][j].from = size + 2 - graph.graph[size - j][size - i].destination; 
            reverse.graph[i][j].destination = size + 2 - graph.graph[size - j][size - i].from; 
        }
    }
    // PrintGraph(reverse); 
    int container_id = 1; 
    float iso = 0;
    queue<int> v;
    bool visited[graph.vertex_num];
    int container[graph.vertex_num];
    for (int i = 0; i < graph.vertex_num; i ++)
    {
        visited[i] = false;
        container[i] = 0; 
    }
    for (int i = 0; i < graph.vertex_num; i ++)
    {
        if (!visited[i])
        {
            visited[i] = true; 
            container[i] = container_id; 
            v.push(i); 
            while (!v.empty())
            {
                int victim = v.front();
                v.pop();
                priority_queue<Parameter_t, vector<Parameter_t>, compare_edge> pq; 
                for (int j = 0; j < graph.vertex_num; j ++)
                {
                    if (!visited[j] && reverse.graph[victim][j].weight != -1)
                    {
                        pq.push(reverse.graph[victim][j]);
                    }
                }
                
                while (!pq.empty())
                {
                    Parameter_t tmp = pq.top();
                    pq.pop();
                    visited[tmp.destination - 1] = true;
                    if (iso + reverse.graph[victim][tmp.destination - 1].isolation >= 1.5)
                    {
                        container_id ++; 
                        container[tmp.destination - 1] = container_id; 
                        iso = 0; 
                    }
                    else
                    {
                        iso += reverse.graph[victim][tmp.destination - 1].isolation; 
                        container[tmp.destination - 1] = container_id; 
                    }
                    v.push(tmp.destination - 1); 
                }
            }
        }
    }
    for (int i = graph.vertex_num - 1; i >= 0; i --)
    {
        cout << container[i] << " "; 
    }
    cout << endl; 
}

void BFS(Graph_t &graph)
{
    // PrintGraph(graph);
    int container_id = 1; 
    float iso = 0;
    queue<int> v;
    bool visited[graph.vertex_num];
    int container[graph.vertex_num];
    for (int i = 0; i < graph.vertex_num; i ++)
    {
        visited[i] = false;
        container[i] = 0; 
    }
    for (int i = 0; i < graph.vertex_num; i ++)
    {
        if (!visited[i])
        {
            visited[i] = true; 
            container[i] = container_id; 
            v.push(i); 
            while (!v.empty())
            {
                int victim = v.front();
                v.pop();
                priority_queue<Parameter_t, vector<Parameter_t>, compare_edge> pq; 
                for (int j = 0; j < graph.vertex_num; j ++)
                {
                    if (!visited[j] && graph.graph[victim][j].weight != -1)
                    {
                        pq.push(graph.graph[victim][j]);
                    }
                }
                
                while (!pq.empty())
                {
                    Parameter_t tmp = pq.top();
                    pq.pop();
                    visited[tmp.destination - 1] = true;
                    if (iso + graph.graph[victim][tmp.destination - 1].isolation >= 1.5)
                    {
                        container_id ++; 
                        container[tmp.destination - 1] = container_id; 
                        iso = 0; 
                    }
                    else
                    {
                        iso += graph.graph[victim][tmp.destination - 1].isolation; 
                        container[tmp.destination - 1] = container_id; 
                    }
                    v.push(tmp.destination - 1); 
                }
            }
        }
    }
    for (int i = 0; i < graph.vertex_num; i ++)
    {
        cout << container[i] << " "; 
    }
    cout << endl; 
}

void BFS_order(Graph_t &graph)
{
    // PrintGraph(graph);
    int container_id = 1; 
    float iso = 0;
    queue<int> v;
    bool visited[graph.vertex_num];
    int container[graph.vertex_num];
    for (int i = 0; i < graph.vertex_num; i ++)
    {
        visited[i] = false;
        container[i] = 0; 
    }
    for (int i = 0; i < graph.vertex_num; i ++)
    {
        if (!visited[i])
        {
            visited[i] = true; 
            container[i] = container_id; 
            v.push(i); 
            while (!v.empty())
            {
                int victim = v.front();
                v.pop();
                for (int j = 0; j < graph.vertex_num; j ++)
                {
                    if (!visited[j] && graph.graph[victim][j].weight != -1)
                    {
                        visited[j] = true;
                        if (iso + graph.graph[victim][j].isolation >= 1.5)
                        {
                            container_id ++; 
                            container[j] = container_id; 
                            iso = 0; 
                        }
                        else
                        {
                            iso += graph.graph[victim][j].isolation; 
                            container[j] = container_id; 
                        }
                        v.push(j); 
                    }
                }
            }
        }
    }
    for (int i = 0; i < graph.vertex_num; i ++)
    {
        cout << container[i] << " "; 
    }
    cout << endl; 
}

void BFS_one(Graph_t &graph)
{
    int container[graph.vertex_num];
    for (int i = 0; i < graph.vertex_num; i ++)
    {
        container[i] = i + 1; 
        cout << container[i] << " "; 
    }
    cout << endl; 
}

void BFS_in_order(Graph_t &graph)
{
    float iso = 0; 
    int host = 0; 
    int container_id = 0; 
    int container[graph.vertex_num];
    for (int i = 0; i < graph.vertex_num; i ++)
    {
        container[i] = 0;
    }
    for (int i = 0; i < graph.vertex_num; i ++)
    {
        if (iso + graph.graph[host][i].isolation >= 1.5)
        {
            host = i;
            iso = 0; 
            container_id ++;
            container[i] = container_id; 
        }
        else
        {
            container[i] = container_id;
            iso += graph.graph[host][i].isolation;
        }
    }
    for (int i = 0; i < graph.vertex_num; i ++)
    {
        cout << container[i] << " "; 
    }
    cout << endl; 
}

int main()
{
    srand((unsigned)time(nullptr)); 
    int vertex_num = 10;
    Graph_t graph; 
    graph.GraphSize(vertex_num); 
    graph.InitializeGraph();  
    VertexInGraph(graph); 
    vector<Core_t *> schedule; 
    InitializeSchedule(schedule); 
    InitializeIso(graph); 
    InitializeIdel(graph, schedule); 

    BFS(graph);
    BFS_reverse(graph); 
    BFS_in_order(graph); 
    return 0; 
}