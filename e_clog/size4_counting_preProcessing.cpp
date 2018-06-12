#include "graph.cpp"

using namespace std;


inline int nChoose2(int n)
{
	if(n%2 == 0)
		return (n/2) * (n-1);
	else
		return n * ((n-1)/2); 
}




/*
edge (u,v)
NodeID_TYPE u, NodeID_TYPE v

graph in CSR formate
NodeID_TYPE* &start_idx,NodeID_TYPE* &nei_size, NodeID_TYPE* & target_node_id

RETURN Triangles (T), Neighbors of only u (N_u), Neighbors of only v (N_v)
vector<NodeID_TYPE> &T,vector<NodeID_TYPE> &N_u,vector<NodeID_TYPE> &N_v

RETURN (Neighbor interesection with T,N_u,N_v) for each node of u,v neoghbors.
unordered_map<NodeID_TYPE,vector<NodeID_TYPE> > &T_key,
unordered_map<NodeID_TYPE,vector<NodeID_TYPE> > &N_u_key,
unordered_map<NodeID_TYPE,vector<NodeID_TYPE> > &N_v_key
//*/

vector<Count_TYPE> get_freqency_vector(NodeID_TYPE u, NodeID_TYPE v,graph & g,vector<NodeID_TYPE> &T,vector<NodeID_TYPE> &N_u,vector<NodeID_TYPE> &N_v,unordered_map<NodeID_TYPE,vector<NodeID_TYPE> > &T_key,unordered_map<NodeID_TYPE,vector<NodeID_TYPE> > &N_u_key,unordered_map<NodeID_TYPE,vector<NodeID_TYPE> > &N_v_key,vector<int> & status_map)
{
//	cout << u << '-' << v <<endl;
//	cout.flush();

	NodeID_TYPE w,r;

//	int* freq = new int[graphlet_count]();				// allocate memory and assigne all values to 0
	vector<Count_TYPE> freq (graphlet_count);				// allocate memory and assigne all values to 0

	status_map[u] = -1;
	status_map[v] = -2;

//	cout << u << " Neighbors: " ;
	for(int i =0; i < g.nei_size[u]; i++)
	{
		w = g.target_node_id[g.start_idx[u]+i];
//		cout << w << ",";
		if(w == v)
			continue;
		N_u.push_back(w);
		status_map[w] = 1;
	}
//	cout <<endl;
//	cout << v << " Neighbors: " ;

	for(int i =0; i < g.nei_size[v]; i++)
	{
		w = g.target_node_id[g.start_idx[v]+i];
//		cout << w << ",";
		if(w == u)
			continue;
		if(status_map[w] == 1)
		{
			vector<NodeID_TYPE>::iterator it1 = find (N_u.begin(), N_u.end(), w);
			N_u.erase(it1);
			T.push_back(w);
			status_map[w] = 3;
		}
		else
		{
			N_v.push_back(w);
			status_map[w] = 2;
		}
	}
//	cout <<endl;
	freq[1] = T.size();
	freq[0] = N_u.size() + N_v.size();

	for(int i = 0 ; i < T.size();i++)
	{
		vector<NodeID_TYPE> T_w,N_u_w,N_v_w;
		w = T[i];
		for(int j =0; j < g.nei_size[w]; j++)
		{
			r = g.target_node_id[g.start_idx[w]+j];

			if(r == u || r == v)
				continue;

			if(status_map[r] == 3)
			{
				T_w.push_back(r);
				freq[11]++;
			}
			else if(status_map[r] == 1)
				N_u_w.push_back(r);
			else if(status_map[r] == 2)
				N_v_w.push_back(r);
			else if(status_map[r] == 4)
				T_w.push_back(r);
			else if(status_map[r] == 0)
				freq[7]++;
			else
				printf("status_map Error!!!\n");
		}
		status_map[w] = 4;
		T_key[w] = T_w;
		N_u_key[w] = N_u_w;
		N_v_key[w] = N_v_w;
	}
//	vector<unsigned long> N_u_counter (N,0);
//	Count_TYPE N_u_new = 0;
	for(int i = 0 ; i < N_u.size();i++)
	{
		vector<NodeID_TYPE> T_w,N_u_w,N_v_w;
		w = N_u[i];
		for(int j =0; j < g.nei_size[w]; j++)
		{
			r = g.target_node_id[g.start_idx[w]+j];
			if(r == u)
				continue;

			if(status_map[r] == 1)
			{
				N_u_w.push_back(r);
				freq[6]++;
			}
			else if(status_map[r] == 2)
			{
				N_v_w.push_back(r);
				freq[5]++;
			}
			else if(status_map[r] == 4)
			{
				T_w.push_back(r);
				freq[9]++;
			}
			else if(status_map[r] == 5)
				N_u_w.push_back(r);
			else if(status_map[r] == 0)
			{
//				status_map[r] = 7;
//				N_u_counter[r] = 1;
//				N_u_new++;
				freq[3]++;
			}
/*
			else if(status_map[r] == 7)
			{
				N_u_counter[r]+=1;
				N_u_new++;
				freq[10]++;
			}
//*/
//			else
//				printf("status_map Error!!!\n");
		}
		status_map[w] = 5;
		T_key[w] = T_w;
		N_u_key[w] = N_u_w;
		N_v_key[w] = N_v_w;
	}

//	Count_TYPE N_v_new = 0;
//	Count_TYPE N_u_minus = 0;
//	Count_TYPE N_v_minus = 0;

	Count_TYPE cycle_5 = 0;

	for(int i = 0 ; i < N_v.size();i++)
	{
		vector<NodeID_TYPE> T_w,N_u_w,N_v_w;
		w = N_v[i];
		for(int j =0; j < g.nei_size[w]; j++)
		{
			r = g.target_node_id[g.start_idx[w]+j];
			if(r == v)
				continue;

			if(status_map[r] == 2)
			{
				N_v_w.push_back(r);
				freq[6]++;
			}
			else if(status_map[r] == 4)
			{
				T_w.push_back(r);
				freq[9]++;
			}
			else if(status_map[r] == 5)
				N_u_w.push_back(r);
			else if(status_map[r] == 6)
				N_v_w.push_back(r);

			else if(status_map[r] == 0)
			{
				freq[3]++;
//				N_v_new++;
			}
/*
			else if(status_map[r] == 7)
			{
				N_v_new++;
				freq[10]++;
				cycle_5 += N_u_counter[r];
			}
//*/
/*

			else if(status_map[r] == 0)
			{
				status_map[r] = 8;
				freq[10]++;
				N_v_new++;
			}
			else if(status_map[r] == 8)
			{
				N_v_new++;
				freq[10]++;
			}
			else if(status_map[r] == 7)
			{
				status_map[r] = 9;
				N_v_new++;
				freq[10]++;
				N_u_minus++;
				N_v_minus += N_u_counter[r];
				cycle_5 += N_u_counter[r];
			}
			else if(status_map[r] == 9)
			{
				N_v_new++;
				freq[10]++;
				N_u_minus++;
				N_v_minus += N_u_counter[r];
				cycle_5 += N_u_counter[r];
			}
//*/
//			else
//				printf("status_map Error!!!\n");
		}
		status_map[w] = 6;
		T_key[w] = T_w;
		N_u_key[w] = N_u_w;
		N_v_key[w] = N_v_w;
	}

	//new
	freq[8] = freq[0]*freq[1] - freq[9];

	//old
	freq[10] = nChoose2(freq[1]) - freq[11];
	if(nChoose2(freq[1]) < freq[11])
		freq[10] = 0;
	freq[2] = (N_u.size() * N_v.size()) - freq[5];
	
	freq[4] = nChoose2(N_u.size()) + nChoose2(N_v.size()) - freq[6];
	if( (nChoose2(N_u.size()) + nChoose2(N_v.size())) < freq[6])
		freq[4] = 0;
	
	return freq;
}

