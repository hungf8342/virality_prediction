#ifndef GRAPH_CPP_
#define GRAPH_CPP_

#include "headers.h"
#include <deque>

using namespace std;


class graph
{


	void local_bfs(vector<NodeID_TYPE> & parent,NodeID_TYPE start)
	{
		deque<NodeID_TYPE> q;
		parent[start] = start;
		q.push_back(start);
		while (!q.empty())
		{
			NodeID_TYPE vertex = q.front();
			q.pop_front();
			for(int i =0; i < nei_size[vertex]; i++)
			{
				NodeID_TYPE v = target_node_id[start_idx[vertex]+1];
				if(parent[v] == -1)
				{
					parent[v] = vertex;
					q.push_back(v);
				}
			}
		}
	}
public:
	NodeID_TYPE N,M;						// N = number of vertices ; M = number of edges
	vector<NodeID_TYPE> * adj_list;					// adj list format
	NodeID_TYPE *start_idx, *nei_size, *target_node_id;			// sparce row major format
	vector<double> degree_propotion;

	graph()
	{
		N = M = 0;
		adj_list = NULL;
		start_idx = NULL;
		nei_size = NULL;
		target_node_id = NULL;
	}
	graph(NodeID_TYPE n, NodeID_TYPE m)
	{
		N = n;
		M = m;
	}
	~graph()
	{
		if(adj_list != NULL)
			delete[] adj_list;
		if(start_idx != NULL)
			delete[] start_idx;
		if(nei_size != NULL)
			delete[] nei_size;
		if(target_node_id != NULL)
			delete[] target_node_id;
	}
	void init_graph(NodeID_TYPE n, NodeID_TYPE m)
	{
		N = n;
		M = m;
	}
	void init()
	{
		start_idx = new NodeID_TYPE[N];
		nei_size = new NodeID_TYPE[N];
		target_node_id = new NodeID_TYPE[2*M];
		if (start_idx == NULL || nei_size == NULL || target_node_id == NULL)
		{
			printf("Error: memory allocation failed!\n");
			exit(1);
		}
	}
	double make_adjList(vector<pair<NodeID_TYPE,NodeID_TYPE> > & edge_list)
	{
		Runtimecounter rt1;
		rt1.start();
		if(N == 0)
		{
			cout << "Error: Initialize number of vertices and number of edges.";
			exit(1);
		}
		adj_list = new vector<NodeID_TYPE>[N];
		if (adj_list == NULL)
		{
			printf("Error: memory allocation failed!\n");
			exit(1);
		}
		NodeID_TYPE u,v;

		for(NodeID_TYPE i =0 ; i < edge_list.size() ; i++ )
		{
			u = edge_list[i].first;
			v = edge_list[i].second;

			adj_list[u].push_back(v);
			adj_list[v].push_back(u);

/*			// add for u to v edge
			auto iter = edges.find(u);
			if(iter != edges.end())
			{
				iter->second.push_back(v);
			}
			else
			{
				vector<NodeID_TYPE>  new_list;
				new_list.push_back(v);
				edges[u] = new_list;
			}
			// add for v to u edge as well		
			iter = edges.find(v);
			if(iter != edges.end())
			{
				iter->second.push_back(u);
			}
			else
			{
				vector<NodeID_TYPE> new_list;
				new_list.push_back(u);
				edges[v] = new_list;
			}
//*/
		}
		rt1.stop();
		double conversion_time = rt1.GetRuntime();
	
		return conversion_time;
	}

	double sort_edges()
	{
		Runtimecounter rt1;
		rt1.start();
		for(NodeID_TYPE i = 0;i < N; i++) 
		{
			sort(adj_list[i].begin(),adj_list[i].end());
		}
		rt1.stop();
		double sort_time = rt1.GetRuntime();
		return sort_time;
	}
	double convert_to_sparse()
	{
		NodeID_TYPE edge_count = 0;
		Runtimecounter rt1;
		rt1.start();
		init();
		NodeID_TYPE counter = 0;
		for(NodeID_TYPE i = 0 ; i < N ; i++)
		{
			start_idx[i] = counter;
			if(adj_list[i].size() == 0)
			{
				nei_size[i] = 0;
				continue;
			}
			nei_size[i] = adj_list[i].size();
			for(int j=0; j < adj_list[i].size(); j++)
			{
				target_node_id[counter++] = adj_list[i][j];
			}
			edge_count += nei_size[i];
		}
		M = edge_count/2;
		rt1.stop();
		double convert_time = rt1.GetRuntime();
		if(adj_list != NULL)
		{
			delete[] adj_list;
			adj_list = NULL;
		}

		return convert_time;
	}
	void del_graph()
	{
		if(adj_list != NULL)
			delete[] adj_list;
		if(start_idx != NULL)
			delete[] start_idx;
		if(nei_size != NULL)
			delete[] nei_size;
		if(target_node_id != NULL)
			delete[] target_node_id;
	}
	NodeID_TYPE get_edge_degreeSum(pair<NodeID_TYPE,NodeID_TYPE> edge)
	{
		return nei_size[edge.first] + nei_size[edge.second];
	}
	bool has_edge(NodeID_TYPE a, NodeID_TYPE b)
	{
		if(nei_size[a] == 0 || nei_size[b] == 0)
			return false;
		if(nei_size[a] < nei_size[b])
		{
			return binary_search(target_node_id+start_idx[a],target_node_id+start_idx[a]+nei_size[a],b);
		}
		else
		{
			return binary_search(target_node_id+start_idx[b],target_node_id+start_idx[b]+nei_size[b],a);
		}
	}
//--------------------------------- Never Used for graphlet counting---------------------------------------------
/*
	long double get_total_triples()
	{
		long double grand_total = 0.0;
		for(NodeID_TYPE i = 0 ;i < N ; i++)
		{
			//degree_propotion.push_back((double)nei_size[i]*((double)nei_size[i]-1.0) / 2.0 );
			grand_total += ((double)nei_size[i]*((double)nei_size[i]-1.0) / 2.0 );
		}
		return grand_total;
	}
	long double init_degree_propotional()
	{
		long double grand_total = 0.0;
		for(NodeID_TYPE i = 0 ;i < N ; i++)
		{
			degree_propotion.push_back((double)nei_size[i]*((double)nei_size[i]-1.0) / 2.0 );
			grand_total += degree_propotion[i];
		}
		
		long double sum = 0.0;
		for(NodeID_TYPE i = 0 ;i < N ; i++)
		{
			sum += degree_propotion[i];
			degree_propotion[i] = sum / grand_total;
		}
//		srand (time(NULL));
		return grand_total;
	}
	NodeID_TYPE get_degree_propotional_vertex()
	{
/*
		vector<double>::iterator low;
		NodeID_TYPE ret_val;
		do{
			double val = (double)rand()/(double)RAND_MAX;
			low = std::lower_bound (degree_propotion.begin(), degree_propotion.end(), val);
			ret_val = (low-degree_propotion.begin())-1;
		}
		while(ret_val >= N);
		return ret_val;
//* /
		return randomWithDiscreteProbability(degree_propotion);
	}

	NodeID_TYPE get_random_neighbor(NodeID_TYPE u)
	{
		int val = boost_get_a_random_number(0, nei_size[u]); 		//rand() % nei_size[u];
		return target_node_id[start_idx[u]+val];
	}

	unsigned long long neighborhood_intersection(NodeID_TYPE x, NodeID_TYPE y, vector<NodeID_TYPE> & Nx_y, vector<NodeID_TYPE> & Ny_x, vector<NodeID_TYPE> & Nxy)
	{
		unsigned long long ret = 0;
		int i = 0;
		int j = 0;
		while(i < nei_size[x] && j < nei_size[y])
		{
			if(target_node_id[i+ start_idx[x]] == target_node_id[j+ start_idx[y]])
			{
				Nxy.push_back(target_node_id[i+ start_idx[x]]);
				ret++;
				i++;
				j++;
			}
			else if(target_node_id[i+ start_idx[x]] < target_node_id[j+ start_idx[y]])
			{
				Nx_y.push_back(target_node_id[i+ start_idx[x]]);
				i++;
			}
			else
			{
				Ny_x.push_back(target_node_id[j+ start_idx[y]]);
				j++;
			}
		}
		while(i < nei_size[x])
		{
			Nx_y.push_back(target_node_id[i+ start_idx[x]]);
			i++;
		}
		while(j < nei_size[y])
		{
			Ny_x.push_back(target_node_id[j+ start_idx[y]]);
			j++;
		}

		return ret;
	}
	void bfs(vector<NodeID_TYPE> & parent)
	{
		for(int i = 0 ;i < N ; i++)
		{
			if(parent[i]== -1)
			{
				local_bfs(parent,i);
			}
		}
	}
//*/

};
#endif 
