#include "graph.cpp"

using namespace std;

vector<NodeID_TYPE> intersection(vector<NodeID_TYPE> a, vector<NodeID_TYPE> b)
{
/*	// currently not neccessary to check this
	if(!is_sorted(a.begin(),a.end()))
		sort(a.begin(),a.end());
	if(!is_sorted(b.begin(),b.end()))
		sort(b.begin(),b.end());
//*/
	vector<NodeID_TYPE> ret;
	int i = 0;
	int j = 0;
	while(i < a.size() && j < b.size())
	{
		if(a[i] == b[j])
		{
			ret.push_back(a[i]);
			i++;
			j++;
		}
		else if(a[i] < b[j])
			i++;
		else
			j++;
	}
	return ret;
}

vector<unsigned int> intersection(vector<NodeID_TYPE> a, vector<NodeID_TYPE> b, NodeID_TYPE val, int &ret_count)
{
	vector<NodeID_TYPE> ret;
	int i = 0;
	int j = 0;
	ret_count = 0;
	while(i < a.size() && j < b.size())
	{
		if(a[i] == b[j])
		{
			ret.push_back(a[i]);
			if(a[i] > val)
				ret_count ++;
			i++;
			j++;
		}
		else if(a[i] < b[j])
			i++;
		else
			j++;
	}
	return ret;
}

vector<NodeID_TYPE> intersection(NodeID_TYPE x, vector<NodeID_TYPE> b, NodeID_TYPE* &start_idx,NodeID_TYPE* &nei_size, NodeID_TYPE* & target_node_id)
{
/*	// currently not neccessary to check this
	if(!is_sorted(a.begin(),a.end()))
		sort(a.begin(),a.end());
	if(!is_sorted(b.begin(),b.end()))
		sort(b.begin(),b.end());
//*/
	vector<NodeID_TYPE> ret;
	int i = 0;
	int j = 0;
	while(i < nei_size[x] && j < b.size())
	{
		if(target_node_id[i+ start_idx[x]] == b[j])
		{
			ret.push_back(b[j]);
			i++;
			j++;
		}
		else if(target_node_id[i+ start_idx[x]] < b[j])
			i++;
		else
			j++;
	}
	return ret;
}


vector<NodeID_TYPE> set_difference(vector<NodeID_TYPE> a, vector<NodeID_TYPE> b)
{
/*	// currently not neccessary to check this
	if(!is_sorted(a.begin(),a.end()))
		sort(a.begin(),a.end());
	if(!is_sorted(b.begin(),b.end()))
		sort(b.begin(),b.end());
//*/
	vector<NodeID_TYPE> ret;
	int i = 0;
	int j = 0;
	while(i < a.size() && j < b.size())
	{
		if(a[i] == b[j])
		{
			i++;
			j++;
		}
		else if(a[i] < b[j])
		{
			ret.push_back(a[i]);
			i++;
		}
		else
			j++;
	}
	while(i < a.size())
		ret.push_back(a[i++]);


	return ret;
}

void size5_path_cycle(NodeID_TYPE u, NodeID_TYPE v, graph & g, vector<NodeID_TYPE> & T,vector<NodeID_TYPE> & N_u, vector<NodeID_TYPE> & N_v, unordered_map<NodeID_TYPE,vector<NodeID_TYPE> > & T_key, unordered_map<NodeID_TYPE,vector<NodeID_TYPE> > & N_u_key,unordered_map<NodeID_TYPE,vector<NodeID_TYPE> > & N_v_key, vector<Count_TYPE> & freq, vector<int> & status_map)
{
	Count_TYPE f13_i=0,f28_i=0;
	for(int idx = 0 ; idx < N_u.size();idx++)
	{
		Count_TYPE f13_uij=0,f28_ij=0;
		NodeID_TYPE i = N_u[idx];
		vector<NodeID_TYPE> N_v_bar = set_difference(N_v, N_v_key[i]);

		for(int idx1 =0; idx1 < g.nei_size[i]; idx1++)
		{
			NodeID_TYPE j = g.target_node_id[g.start_idx[i]+idx1];
			if(status_map[j] == 0)
			{
				vector<NodeID_TYPE> N_vij_bar = intersection(j,N_v_bar,g.start_idx,g.nei_size,g.target_node_id);
				f28_ij += N_vij_bar.size();
				f13_uij += (N_v_bar.size()-N_vij_bar.size());
			}

		}
		f13_i += f13_uij;
		f28_i += f28_ij;
	}

	for(int idx = 0 ; idx < N_v.size();idx++)
	{
		Count_TYPE f13_vij=0,f28_ij=0;
		NodeID_TYPE i = N_v[idx];
		vector<NodeID_TYPE> N_u_bar = set_difference(N_u, N_u_key[i]);

		for(int idx1 =0; idx1 < g.nei_size[i]; idx1++)
		{
			NodeID_TYPE j = g.target_node_id[g.start_idx[i]+idx1];
			if(status_map[j] == 0)
			{
				vector<NodeID_TYPE> N_uij_bar = intersection(j,N_u_bar,g.start_idx,g.nei_size,g.target_node_id);
//				f28_ij += N_uij_bar.size();
				f13_vij += (N_u_bar.size()-N_uij_bar.size());
			}
		}
		f13_i += f13_vij;
//		f28_i += f28_ij;
	}

	freq[12] = f13_i;
	freq[19] = f28_i;
//	freq[19] = f28_i/2;

}

void algorithm1236(NodeID_TYPE u, NodeID_TYPE v,vector<NodeID_TYPE> & T,vector<NodeID_TYPE> & N_u,vector<NodeID_TYPE> & N_v,unordered_map<NodeID_TYPE,vector<NodeID_TYPE> > & T_key,unordered_map<NodeID_TYPE,vector<NodeID_TYPE> > & N_u_key,unordered_map<NodeID_TYPE,vector<NodeID_TYPE> > & N_v_key, vector<Count_TYPE> & freq)
{
	//algo1
	Count_TYPE f67_i=0,f66_i=0,f60_i=0,f50_i=0;
	//algo6
	Count_TYPE f48_i=0,f33_i=0,f26_i=0,f19_i=0;
	Count_TYPE f44_i=0;
	//algo2
	Count_TYPE f65_i=0,f64_i=0,f61_i=0,f54_i=0;
	//algo3
	Count_TYPE f59_i=0,f52_i=0,f47_i=0,f34_i=0;
	Count_TYPE f63_i=0,f56_i=0,f55_i=0,f40_i=0;
	int error_counter = 0 ;
	for(int idx =0; idx < T.size();idx++)
	{
	// algo1
		NodeID_TYPE i = T[idx];
		Count_TYPE f67_ij=0,f66_ij=0,f60_ij=0,f50_uij=0,f50_vij=0;
		for(int idx1 = 0; idx1 < T_key[i].size(); idx1++)
		{
			NodeID_TYPE j = T_key[i][idx1];
			if(j < i)
			{
				vector<NodeID_TYPE> N_Tij = intersection(T_key[i],T_key[j]);
				f66_ij += T_key[j].size() - N_Tij.size() -1;
				continue;
			}

			// k in T
			int inter_size;
			vector<NodeID_TYPE> N_Tij = intersection(T_key[i],T_key[j],j,inter_size);
			f67_ij += inter_size;
			f66_ij += T_key[j].size() - N_Tij.size() -1;
			f60_ij += T.size() - T_key[i].size() - T_key[j].size() + N_Tij.size();
			// k in N_u
			vector<NodeID_TYPE> N_uij = intersection(N_u_key[i],N_u_key[j]);
			f50_uij += N_u.size() - N_u_key[i].size() - N_u_key[j].size() + N_uij.size();
			// k in N_v
			vector<NodeID_TYPE> N_vij = intersection(N_v_key[i],N_v_key[j]);
			f50_vij += N_v.size() - N_v_key[i].size() - N_v_key[j].size() + N_vij.size();
		}
//		if(f67_ij % 2 != 0)
//			error_counter++;
//		f67_i = f67_i + (f67_ij/2);
		f67_i = f67_i + f67_ij;
		f66_i = f66_i + f66_ij;
		f60_i = f60_i + f60_ij;
		f50_i = f50_i + f50_uij + f50_vij;

	// algo6
		Count_TYPE f48_ij=0,f33_uij=0,f33_vij=0;
		// j in T (N_Ti_bar)
		vector<NodeID_TYPE> temp_T;
		for(int k = 0 ;k < T.size();k++)
		{
			if(T[k] != i)
				temp_T.push_back(T[k]); 
		}
		vector<NodeID_TYPE> N_Ti_bar = set_difference(temp_T,T_key[i]);
		for(int idx1 = 0; idx1 < N_Ti_bar.size(); idx1++)
		{
			NodeID_TYPE j = N_Ti_bar[idx1];
			// k in T
			vector<NodeID_TYPE> N_Tij = intersection(T_key[i],T_key[j]);
			f48_ij += T.size() - T_key[i].size() - T_key[j].size() + N_Tij.size() - 2;
			// k in N_u
			vector<NodeID_TYPE> N_uij = intersection(N_u_key[i],N_u_key[j]);
			f33_uij += N_u.size() - N_u_key[i].size() - N_u_key[j].size() + N_uij.size();
			// k in N_v
			vector<NodeID_TYPE> N_vij = intersection(N_v_key[i],N_v_key[j]);
			f33_vij += N_v.size() - N_v_key[i].size() - N_v_key[j].size() + N_vij.size();
		}
//		if(f48_ij % 2 != 0)
//			error_counter++;
		f48_i = f48_i + (f48_ij/2);
		f33_i = f33_i + f33_uij + f33_vij;

		// j in N_u (N_ui_bar)
		vector<NodeID_TYPE> N_ui_bar = set_difference(N_u,N_u_key[i]);
		Count_TYPE f26_uij=0,f26_vij=0,f19_ij=0;
		Count_TYPE f44_ij=0;
		for(int idx1 = 0; idx1 < N_ui_bar.size(); idx1++)
		{
			NodeID_TYPE j = N_ui_bar[idx1];
			// k in N_u
			vector<NodeID_TYPE> N_uij = intersection(N_u_key[i],N_u_key[j]);
			f26_uij += N_u.size() - N_u_key[i].size() - N_u_key[j].size() + N_uij.size() -1;
			// k in N_v
			vector<NodeID_TYPE> N_vij = intersection(N_v_key[i],N_v_key[j]);
			f44_ij += N_v_key[j].size() - N_vij.size();
			f19_ij += N_v.size() - N_v_key[i].size() - N_v_key[j].size() + N_vij.size();
		}
//		if(f26_uij % 2 != 0)
//			error_counter++;
		f26_i = f26_i + (f26_uij/2);
		f19_i = f19_i + f19_ij;
		f44_i = f44_i + f44_ij;
		// j in N_v (N_vi_bar)
		vector<NodeID_TYPE> N_vi_bar = set_difference(N_v,N_v_key[i]);
		for(int idx1 = 0; idx1 < N_vi_bar.size(); idx1++)
		{
			NodeID_TYPE j = N_vi_bar[idx1];
			// k in N_v
			vector<NodeID_TYPE> N_vij = intersection(N_v_key[i],N_v_key[j]);
			f26_vij += N_v.size() - N_v_key[i].size() - N_v_key[j].size() + N_vij.size() -1;
		}
//		if(f26_vij % 2 != 0)
//			error_counter++;
		f26_i = f26_i + (f26_vij/2);

	//algo2   j in N_u
		Count_TYPE f65_ij_u=0,f64_ij_u=0,f61_ij_u=0,f54_ij_u=0;
	//algo3  j in N_u
		Count_TYPE f59_ij_u=0,f52_ij_u=0,f47_ij_u=0,f34_ij_u=0;
		Count_TYPE f63_ij_u=0,f56_ij_u=0,f55_ij_u=0,f40_ij_u=0;
		for(int idx1 = 0; idx1 < N_u_key[i].size(); idx1++)
		{
			NodeID_TYPE j = N_u_key[i][idx1];
			// k in T
			vector<NodeID_TYPE> N_Tij = intersection(T_key[i],T_key[j]);
			f65_ij_u += N_Tij.size();
			f64_ij_u += T_key[j].size() - N_Tij.size() -1;
			f61_ij_u += T_key[i].size() - N_Tij.size();
			f54_ij_u += T.size() - T_key[i].size() - T_key[j].size() + N_Tij.size();

			// algo3
			// k in N_u
			vector<NodeID_TYPE> N_uij = intersection(N_u_key[i],N_u_key[j]);
			f59_ij_u += N_uij.size();
			f52_ij_u += N_u_key[j].size() - N_uij.size();
			f47_ij_u += N_u_key[i].size() - N_uij.size() - 1;
			f34_ij_u += N_u.size() - N_u_key[i].size() - N_u_key[j].size() + N_uij.size();
			// k in N_v
			vector<NodeID_TYPE> N_vij = intersection(N_v_key[i],N_v_key[j]);
			f63_ij_u += N_vij.size();
			f56_ij_u += N_v_key[j].size() - N_vij.size();
			f55_ij_u += N_v_key[i].size() - N_vij.size();
			f40_ij_u += N_v.size() - N_v_key[i].size() - N_v_key[j].size() + N_vij.size();


		}
		f65_i = f65_i + f65_ij_u;
		f64_i = f64_i + f64_ij_u;
		f61_i = f61_i + f61_ij_u;
		f54_i = f54_i + f54_ij_u;


//		if(f59_ij_u % 2 != 0)
//			error_counter++;
//		if(f47_ij_u % 2 != 0)
//			error_counter++;
		f59_i = f59_i + f59_ij_u/2;
		f52_i = f52_i + f52_ij_u;
		f47_i = f47_i + f47_ij_u/2;
		f34_i = f34_i + f34_ij_u;
		f63_i = f63_i + f63_ij_u;
		f56_i = f56_i + f56_ij_u;
		f55_i = f55_i + f55_ij_u;
		f40_i = f40_i + f40_ij_u;

	//algo2   j in N_v
		Count_TYPE f65_ij_v=0,f64_ij_v=0,f61_ij_v=0,f54_ij_v=0;
	//algo3  j in N_v
		Count_TYPE f59_ij_v=0,f52_ij_v=0,f47_ij_v=0,f34_ij_v=0;
		Count_TYPE f56_ij_v=0,f40_ij_v=0;
		for(int idx1 = 0; idx1 < N_v_key[i].size(); idx1++)
		{
			NodeID_TYPE j = N_v_key[i][idx1];
			// k in T
			vector<NodeID_TYPE> N_Tij = intersection(T_key[i],T_key[j]);
			f65_ij_v += N_Tij.size();
			f64_ij_v += T_key[j].size() - N_Tij.size() -1;
			f61_ij_v += T_key[i].size() - N_Tij.size();
			f54_ij_v += T.size() - T_key[i].size() - T_key[j].size() + N_Tij.size();

			// algo3
			// k in N_v
			vector<NodeID_TYPE> N_vij = intersection(N_v_key[i],N_v_key[j]);
			f59_ij_v += N_vij.size();
			f52_ij_v += N_v_key[j].size() - N_vij.size();
			f47_ij_v += N_v_key[i].size() - N_vij.size() - 1;
			f34_ij_v += N_v.size() - N_v_key[i].size() - N_v_key[j].size() + N_vij.size();
			// k in N_u
			vector<NodeID_TYPE> N_uij = intersection(N_u_key[i],N_u_key[j]);
			f56_ij_v += N_u_key[j].size() - N_uij.size();
			f40_ij_v += N_u.size() - N_u_key[i].size() - N_u_key[j].size() + N_uij.size();

		}
		f65_i = f65_i + f65_ij_v;
		f64_i = f64_i + f64_ij_v;
		f61_i = f61_i + f61_ij_v;
		f54_i = f54_i + f54_ij_v;

//		if(f59_ij_u % 2 != 0)
//			error_counter++;
//		if(f47_ij_u % 2 != 0)
//			error_counter++;
		f59_i = f59_i + f59_ij_v/2;
		f52_i = f52_i + f52_ij_v;
		f47_i = f47_i + f47_ij_v/2;
		f34_i = f34_i + f34_ij_v;
		f56_i = f56_i + f56_ij_v;
		f40_i = f40_i + f40_ij_v;

/*

	//algo3  j in N_u
		Count_TYPE f59_ij_u=0,f52_ij_u=0,f47_ij_u=0,f34_ij_u=0;
		Count_TYPE f63_ij_u=0,f56_ij_u=0,f55_ij_u=0,f40_ij_u=0;
		for(int idx1 = 0; idx1 < N_u_key[i].size(); idx1++)
		{
			NodeID_TYPE j = N_u_key[i][idx1];
			// k in N_u
			vector<NodeID_TYPE> N_uij = intersection(N_u_key[i],N_u_key[j]);
			f59_ij_u += N_uij.size();
			f52_ij_u += N_u_key[j].size() - N_uij.size();
			f47_ij_u += N_u_key[i].size() - N_uij.size() - 1;
			f34_ij_u += N_u.size() - N_u_key[i].size() - N_u_key[j].size() + N_uij.size();
			// k in N_v
			vector<NodeID_TYPE> N_vij = intersection(N_v_key[i],N_v_key[j]);
			f63_ij_u += N_vij.size();
			f56_ij_u += N_v_key[j].size() - N_vij.size();
			f55_ij_u += N_v_key[i].size() - N_vij.size();
			f40_ij_u += N_v.size() - N_v_key[i].size() - N_v_key[j].size() + N_vij.size();

		}
//		if(f59_ij_u % 2 != 0)
//			error_counter++;
//		if(f47_ij_u % 2 != 0)
//			error_counter++;
		f59_i = f59_i + f59_ij_u/2;
		f52_i = f52_i + f52_ij_u;
		f47_i = f47_i + f47_ij_u/2;
		f34_i = f34_i + f34_ij_u;
		f63_i = f63_i + f63_ij_u;
		f56_i = f56_i + f56_ij_u;
		f55_i = f55_i + f55_ij_u;
		f40_i = f40_i + f40_ij_u;
	//algo3  j in N_v
		Count_TYPE f59_ij_v=0,f52_ij_v=0,f47_ij_v=0,f34_ij_v=0;
		Count_TYPE f56_ij_v=0,f40_ij_v=0;
		for(int idx1 = 0; idx1 < N_v_key[i].size(); idx1++)
		{
			NodeID_TYPE j = N_v_key[i][idx1];
			// k in N_v
			vector<NodeID_TYPE> N_vij = intersection(N_v_key[i],N_v_key[j]);
			f59_ij_v += N_vij.size();
			f52_ij_v += N_v_key[j].size() - N_vij.size();
			f47_ij_v += N_v_key[i].size() - N_vij.size() - 1;
			f34_ij_v += N_v.size() - N_v_key[i].size() - N_v_key[j].size() + N_vij.size();
			// k in N_u
			vector<NodeID_TYPE> N_uij = intersection(N_u_key[i],N_u_key[j]);
			f56_ij_v += N_u_key[j].size() - N_uij.size();
			f40_ij_v += N_u.size() - N_u_key[i].size() - N_u_key[j].size() + N_uij.size();

		}
//		if(f59_ij_u % 2 != 0)
//			error_counter++;
//		if(f47_ij_u % 2 != 0)
//			error_counter++;
		f59_i = f59_i + f59_ij_v/2;
		f52_i = f52_i + f52_ij_v;
		f47_i = f47_i + f47_ij_v/2;
		f34_i = f34_i + f34_ij_v;
		f56_i = f56_i + f56_ij_v;
		f40_i = f40_i + f40_ij_v;
//*/

	}

//----------------------------------

/*
	if(f67_i % 3 != 0)
		error_counter++;
	if(f66_i % 2 != 0)
		error_counter++;
	if(f60_i % 2 != 0)
		error_counter++;
	if(f50_i % 2 != 0)
		error_counter++;
	if(f48_i % 3 != 0)
		error_counter++;
	if(f33_i % 2 != 0)
		error_counter++;
	if(f65_i % 2 != 0)
		error_counter++;
	if(f64_i % 2 != 0)
		error_counter++;
*/

//	freq[45] = f67_i/3;
//	freq[44] = f66_i/2;
//	freq[39] = f60_i/2;
//	freq[31] = f50_i/2;
	freq[45] = f67_i;
	freq[44] = f66_i/2;
	freq[39] = f60_i;
	freq[31] = f50_i;
	//algo6
	freq[30] = f48_i/3;
	freq[21] = f33_i/2;
	freq[17] = f26_i;
	freq[15] = f19_i;
	freq[27] = f44_i;
	//algo2
	freq[43] = f65_i/2;
	freq[42] = f64_i/2;
	freq[40] = f61_i;
	freq[34] = f54_i;
	//algo3
	freq[38] = f59_i;
	freq[33] = f52_i;
	freq[29] = f47_i;
	freq[22] = f34_i;
	freq[41] = f63_i;
	freq[36] = f56_i;
	freq[35] = f55_i;
	freq[25] = f40_i;

}
void algorithm457(NodeID_TYPE u, NodeID_TYPE v,vector<NodeID_TYPE> &T,vector<NodeID_TYPE> &N_u,vector<NodeID_TYPE> &N_v,unordered_map<NodeID_TYPE,vector<NodeID_TYPE> > &T_key,unordered_map<NodeID_TYPE,vector<NodeID_TYPE> > &N_u_key,unordered_map<NodeID_TYPE,vector<NodeID_TYPE> > &N_v_key, vector<Count_TYPE> &freq)
{
	//algo4
	Count_TYPE f51_i=0,f35_i=0,f27_i=0,f57_i=0,f45_i=0,f23_i=0,f37_i=0;
	//algo5
	Count_TYPE f42_i=0,f30_i=0,f44_i=0;
	//algo7
	Count_TYPE f17_i=0,f15_i=0;
	int error_counter = 0 ;
//i in N_u
	for(int idx =0; idx < N_u.size();idx++)
	{
	// algo4  j in N_u
		NodeID_TYPE i = N_u[idx];
		Count_TYPE f51_ij=0,f35_ij=0,f27_ij=0,f57_ij=0,f45_ij=0,f23_ij=0,f37_ij=0;
		for(int idx1 = 0; idx1 < N_u_key[i].size(); idx1++)
		{
			NodeID_TYPE j = N_u_key[i][idx1];
			if(j < i)
			{
				vector<NodeID_TYPE> N_uij = intersection(N_u_key[i],N_u_key[j]);
				f35_ij += N_u_key[j].size() - N_uij.size() - 1;
				vector<NodeID_TYPE> N_vij = intersection(N_v_key[i],N_v_key[j]);
				f45_ij += N_v_key[j].size() - N_vij.size();
				continue;
			}
			// k in N_u
			int inter_size;
			vector<NodeID_TYPE> N_uij = intersection(N_u_key[i],N_u_key[j],j,inter_size);
			f51_ij += inter_size;
			f35_ij += N_u_key[j].size() - N_uij.size() - 1;
			f27_ij += N_u.size() - N_u_key[i].size() - N_u_key[j].size() + N_uij.size();
			// k in N_v
			vector<NodeID_TYPE> N_vij = intersection(N_v_key[i],N_v_key[j]);
			f57_ij += N_vij.size();
			f45_ij += N_v_key[j].size() - N_vij.size();
			f23_ij += N_v.size() - N_v_key[i].size() - N_v_key[j].size() + N_vij.size();
			// k in T
			vector<NodeID_TYPE> N_Tij = intersection(T_key[i],T_key[j]);
			f37_ij += T.size() - T_key[i].size() - T_key[j].size() + N_Tij.size();
		}
//		if(f51_ij % 2 != 0)
//			error_counter++;
//		f51_i = f51_i + (f51_ij/2);
		f51_i = f51_i + f51_ij;
		f35_i = f35_i + f35_ij;
		f27_i = f27_i + f27_ij;
		f57_i = f57_i + f57_ij;
		f45_i = f45_i + f45_ij;
		f23_i = f23_i + f23_ij;
		f37_i = f37_i + f37_ij;
/*
	//algo5   j in N_v
		Count_TYPE f42_uij=0,f30_uij=0,f42_vij=0,f30_vij=0,f44_ij=0;
		for(int idx1 = 0; idx1 < N_v_key[i].size(); idx1++)
		{
			NodeID_TYPE j = N_v_key[i][idx1];
			// k in N_u
			vector<NodeID_TYPE> N_uij = intersection(N_u_key[i],N_u_key[j]);
			f42_uij += N_u_key[j].size() - N_uij.size() -1;
			f30_uij += N_u.size() - N_u_key[i].size() - N_u_key[j].size() + N_uij.size();
			// k in N_v
			vector<NodeID_TYPE> N_vij = intersection(N_v_key[i],N_v_key[j]);
//			f42_vij += N_v_key[j].size() - N_vij.size() -1;
			f30_vij += N_v.size() - N_v_key[i].size() - N_v_key[j].size() + N_vij.size();
			// k in T
//			vector<NodeID_TYPE> N_Tij = intersection(T_key[i],T_key[j]);
//			f44_ij = T.size() - T_key[i].size() - T_key[j].size() + N_Tij.size();
		}
		f42_i = f42_i + f42_uij + f42_vij;
		f30_i = f30_i + f30_uij + f30_vij;
//		f44_i = f44_i + f44_ij;


//*/
	//algo7   j in N_u (N_ui_bar)
		Count_TYPE f42_ij=0,f30_ij=0;
		Count_TYPE f17_ij=0,f15_ij=0;
		vector<NodeID_TYPE> temp_N_u;
		for(int k = 0 ;k < N_u.size();k++)
		{
			if(N_u[k] != i)
				temp_N_u.push_back(N_u[k]); 
		}
		vector<NodeID_TYPE> N_ui_bar = set_difference(temp_N_u,N_u_key[i]);
		for(int idx1 = 0; idx1 < N_ui_bar.size(); idx1++)
		{
			NodeID_TYPE j = N_ui_bar[idx1];
			// k in N_u
			vector<NodeID_TYPE> N_uij = intersection(N_u_key[i],N_u_key[j]);
			f17_ij += N_u.size() - N_u_key[i].size() - N_u_key[j].size() + N_uij.size() - 2;
			// k in N_v
			vector<NodeID_TYPE> N_vij = intersection(N_v_key[i],N_v_key[j]);
			f42_ij += N_vij.size();
			f30_ij += N_v_key[j].size() - N_vij.size();
			f15_ij += N_v.size() - N_v_key[i].size() - N_v_key[j].size() + N_vij.size();
		}
		f17_i = f17_i + (f17_ij/2);
		f15_i = f15_i + f15_ij;
		f42_i = f42_i + f42_ij;
		f30_i = f30_i + f30_ij;


/*
		Count_TYPE f15_ij_ = 0;
		vector<NodeID_TYPE> N_vi_bar = set_difference(N_v,N_v_key[i]);
		for(int idx1 = 0; idx1 < N_vi_bar.size(); idx1++)
		{
			NodeID_TYPE j = N_vi_bar[idx1];
			// k in N_u
			vector<NodeID_TYPE> N_uij = intersection(N_u_key[i],N_u_key[j]);
			f15_ij_ += N_u.size() - N_u_key[i].size() - N_u_key[j].size() + N_uij.size()-1;
		}
		f15_i = f15_i + f15_ij_;
//*
/*
		Count_TYPE f15_ij_ = 0;
		vector<NodeID_TYPE> N_vi_bar = set_difference(N_v,N_v_key[i]);
		for(int idx1 = 0; idx1 < N_vi_bar.size(); idx1++)
		{
			NodeID_TYPE j = N_vi_bar[idx1];
			// k in N_v
			vector<NodeID_TYPE> N_vij = intersection(N_v_key[i],N_v_key[j]);
			f15_ij_ += N_v.size() - N_v_key[i].size() - N_v_key[j].size() + N_vij.size()-1;
		}
		f15_i = f15_i + (f15_ij_/2);
//*/
	}
//i in N_v
	for(int idx =0; idx < N_v.size();idx++)
	{
	// algo4  j in N_u
		NodeID_TYPE i = N_v[idx];
		Count_TYPE f51_ij=0,f35_ij=0,f27_ij=0,f57_ij=0,f45_ij=0,f23_ij=0,f37_ij=0;
		for(int idx1 = 0; idx1 < N_v_key[i].size(); idx1++)
		{
			NodeID_TYPE j = N_v_key[i][idx1];
			if(j < i)
			{
				vector<NodeID_TYPE> N_vij = intersection(N_v_key[i],N_v_key[j]);
				f35_ij += N_v_key[j].size() - N_vij.size() - 1;
				vector<NodeID_TYPE> N_uij = intersection(N_u_key[i],N_u_key[j]);
				f45_ij += N_u_key[j].size() - N_uij.size();
				continue;
			}
			// k in N_v
			int inter_size;
			vector<NodeID_TYPE> N_vij = intersection(N_v_key[i],N_v_key[j],j,inter_size);
			f51_ij += inter_size;
			f35_ij += N_v_key[j].size() - N_vij.size() - 1;
			f27_ij += N_v.size() - N_v_key[i].size() - N_v_key[j].size() + N_vij.size();
			// k in N_u
			vector<NodeID_TYPE> N_uij = intersection(N_u_key[i],N_u_key[j]);
			f57_ij += N_uij.size();
			f45_ij += N_u_key[j].size() - N_uij.size();
			f23_ij += N_u.size() - N_u_key[i].size() - N_u_key[j].size() + N_uij.size();
			// k in T
			vector<NodeID_TYPE> N_Tij = intersection(T_key[i],T_key[j]);
			f37_ij += T.size() - T_key[i].size() - T_key[j].size() + N_Tij.size();
		}
//		if(f51_ij % 2 != 0)
//			error_counter++;
//		f51_i = f51_i + (f51_ij/2);
		f51_i = f51_i + f51_ij;
		f35_i = f35_i + f35_ij;
		f27_i = f27_i + f27_ij;
		f57_i = f57_i + f57_ij;
		f45_i = f45_i + f45_ij;
		f23_i = f23_i + f23_ij;
		f37_i = f37_i + f37_ij;

/*
	//algo5   j in N_u
		Count_TYPE f42_uij=0,f30_uij=0,f42_vij=0,f30_vij=0,f44_ij=0;
		for(int idx1 = 0; idx1 < N_u_key[i].size(); idx1++)
		{
			NodeID_TYPE j = N_u_key[i][idx1];
			// k in N_v
			vector<NodeID_TYPE> N_vij = intersection(N_v_key[i],N_v_key[j]);
			f42_vij += N_v_key[j].size() - N_vij.size() -1;
//			f30_uij += N_u.size() - N_u_key[i].size() - N_u_key[j].size() + N_uij.size();
			// k in N_u
//			vector<NodeID_TYPE> N_vij = intersection(N_v_key[i],N_v_key[j]);
//			f42_vij += N_v_key[j].size() - N_vij.size() -1;
//			f30_vij += N_v.size() - N_v_key[i].size() - N_v_key[j].size() + N_vij.size();
			// k in T
//			vector<NodeID_TYPE> N_Tij = intersection(T_key[i],T_key[j]);
//			f44_ij = T.size() - T_key[i].size() - T_key[j].size() + N_Tij.size();
		}
		f42_i = f42_i + f42_uij + f42_vij;
//		f30_i = f30_i + f30_uij + f30_vij;
//		f44_i = f44_i + f44_ij;

//*/
	//algo7   j in N_v (N_vi_bar)
		Count_TYPE f42_ij=0,f30_ij=0;
		Count_TYPE f17_ij=0,f15_ij=0;
		vector<NodeID_TYPE> temp_N_v;
		for(int k = 0 ;k < N_v.size();k++)
		{
			if(N_v[k] != i)
				temp_N_v.push_back(N_v[k]); 
		}
		vector<NodeID_TYPE> N_vi_bar = set_difference(temp_N_v,N_v_key[i]);
		for(int idx1 = 0; idx1 < N_vi_bar.size(); idx1++)
		{
			NodeID_TYPE j = N_vi_bar[idx1];
			// k in N_v
			vector<NodeID_TYPE> N_vij = intersection(N_v_key[i],N_v_key[j]);
			f17_ij += N_v.size() - N_v_key[i].size() - N_v_key[j].size() + N_vij.size() - 2;
			// k in N_u
			vector<NodeID_TYPE> N_uij = intersection(N_u_key[i],N_u_key[j]);
			f42_ij += N_uij.size();
			f30_ij += N_u_key[j].size() - N_uij.size();
			f15_ij += N_u.size() - N_u_key[i].size() - N_u_key[j].size() + N_uij.size();
		}
		f17_i = f17_i + (f17_ij/2);
		f15_i = f15_i + f15_ij;
		f42_i = f42_i + f42_ij;
		f30_i = f30_i + f30_ij;

/*
		Count_TYPE f15_ij_ = 0;
		vector<NodeID_TYPE> N_ui_bar = set_difference(N_u,N_u_key[i]);
		for(int idx1 = 0; idx1 < N_ui_bar.size(); idx1++)
		{
			NodeID_TYPE j = N_ui_bar[idx1];
			// k in N_v
			vector<NodeID_TYPE> N_vij = intersection(N_v_key[i],N_v_key[j]);
			f15_ij_ += N_v.size() - N_v_key[i].size() - N_v_key[j].size() + N_vij.size()-1;
		}
		f15_i = f15_i + f15_ij_;
//*
/*

		Count_TYPE f15_ij_ = 0;
		vector<NodeID_TYPE> N_ui_bar = set_difference(N_u,N_u_key[i]);
		for(int idx1 = 0; idx1 < N_ui_bar.size(); idx1++)
		{
			NodeID_TYPE j = N_ui_bar[idx1];
			// k in N_u
			vector<NodeID_TYPE> N_uij = intersection(N_u_key[i],N_u_key[j]);
			f15_ij_ += N_u.size() - N_u_key[i].size() - N_u_key[j].size() + N_uij.size()-1;
		}
		f15_i = f15_i + (f15_ij_/2);
//*/
	}
/*
	if(f51_i % 3 != 0)
		error_counter++;
	if(f35_i % 2!= 0)
		error_counter++;
	if(f27_i % 2!= 0)
		error_counter++;
	if(f57_i % 2!= 0)
		error_counter++;
	if(f23_i % 2!= 0)
		error_counter++;
	if(f37_i % 2!= 0)
		error_counter++;
	if(f42_i % 2!= 0)
		error_counter++;
	if(f17_i % 3!= 0)
		error_counter++;
	if(f15_i % 2!= 0)
		error_counter++;
//*/

	//algo4
//	freq[32] = f51_i/3;
//	freq[23] = f35_i/2;
//	freq[18] = f27_i/2;
//	freq[37] = f57_i/2;
//	freq[28] = f45_i;
//	freq[16] = f23_i/2;
//	freq[24] = f37_i/2;
	freq[32] = f51_i;
	freq[23] = f35_i/2;
	freq[18] = f27_i;
	freq[37] = f57_i;
	freq[28] = f45_i;
	freq[16] = f23_i;
	freq[24] = f37_i;

	//algo5
//	freq[26] = f42_i/2;
//	freq[20] = f30_i;
//	freq[25] = f44_i;
	//algo7
	freq[14] = f17_i/3;
	freq[13] = f15_i/2;
	freq[26] = f42_i/2;
	freq[20] = f30_i;

//	freq[12] = f15_i;

}






//------------------------------------------------------------------------------------------------------------------
// ************ Unique **************
//------------------------------------------------------------------------------------------------------------------

void algorithm1236_unique(NodeID_TYPE u, NodeID_TYPE v,vector<NodeID_TYPE> & T,vector<NodeID_TYPE> & N_u,vector<NodeID_TYPE> & N_v,unordered_map<NodeID_TYPE,vector<NodeID_TYPE> > & T_key,unordered_map<NodeID_TYPE,vector<NodeID_TYPE> > & N_u_key,unordered_map<NodeID_TYPE,vector<NodeID_TYPE> > & N_v_key, vector<Count_TYPE> & freq)
{
	//algo1
	Count_TYPE f67_i=0,f66_i=0,f60_i=0,f50_i=0;
	//algo6
	Count_TYPE f48_i=0,f33_i=0,f26_i=0,f19_i=0;
	Count_TYPE f44_i=0;
	//algo2
//	Count_TYPE f65_i=0,f64_i=0,f61_i=0,f54_i=0;
	//algo3
//	Count_TYPE f59_i=0,f52_i=0,f47_i=0,f34_i=0;
	Count_TYPE f63_i=0,f56_i=0,f55_i=0,f40_i=0;
	int error_counter = 0 ;
	for(int idx =0; idx < T.size();idx++)
	{
	// algo1
		NodeID_TYPE i = T[idx];
		Count_TYPE f67_ij=0,f66_ij=0,f60_ij=0,f50_uij=0,f50_vij=0;
		for(int idx1 = 0; idx1 < T_key[i].size(); idx1++)
		{
			NodeID_TYPE j = T_key[i][idx1];
			if(j < i)
			{
				vector<NodeID_TYPE> N_Tij = intersection(T_key[i],T_key[j]);
				f66_ij += T_key[j].size() - N_Tij.size() -1;
				continue;
			}

			// k in T
			int inter_size;
			vector<NodeID_TYPE> N_Tij = intersection(T_key[i],T_key[j],j,inter_size);
			f67_ij += inter_size;
			f66_ij += T_key[j].size() - N_Tij.size() -1;
			f60_ij += T.size() - T_key[i].size() - T_key[j].size() + N_Tij.size();
			// k in N_u
			vector<NodeID_TYPE> N_uij = intersection(N_u_key[i],N_u_key[j]);
			f50_uij += N_u.size() - N_u_key[i].size() - N_u_key[j].size() + N_uij.size();
			// k in N_v
			vector<NodeID_TYPE> N_vij = intersection(N_v_key[i],N_v_key[j]);
			f50_vij += N_v.size() - N_v_key[i].size() - N_v_key[j].size() + N_vij.size();
		}
//		if(f67_ij % 2 != 0)
//			error_counter++;
//		f67_i = f67_i + (f67_ij/2);
		f67_i = f67_i + f67_ij;
		f66_i = f66_i + f66_ij;
		f60_i = f60_i + f60_ij;
		f50_i = f50_i + f50_uij + f50_vij;

	// algo6
		Count_TYPE f48_ij=0,f33_uij=0,f33_vij=0;
		// j in T (N_Ti_bar)
		vector<NodeID_TYPE> temp_T;
		for(int k = 0 ;k < T.size();k++)
		{
			if(T[k] != i)
				temp_T.push_back(T[k]); 
		}
		vector<NodeID_TYPE> N_Ti_bar = set_difference(temp_T,T_key[i]);
		for(int idx1 = 0; idx1 < N_Ti_bar.size(); idx1++)
		{
			NodeID_TYPE j = N_Ti_bar[idx1];
			// k in T
			vector<NodeID_TYPE> N_Tij = intersection(T_key[i],T_key[j]);
			f48_ij += T.size() - T_key[i].size() - T_key[j].size() + N_Tij.size() - 2;
			// k in N_u
			vector<NodeID_TYPE> N_uij = intersection(N_u_key[i],N_u_key[j]);
			f33_uij += N_u.size() - N_u_key[i].size() - N_u_key[j].size() + N_uij.size();
			// k in N_v
			vector<NodeID_TYPE> N_vij = intersection(N_v_key[i],N_v_key[j]);
			f33_vij += N_v.size() - N_v_key[i].size() - N_v_key[j].size() + N_vij.size();
		}
//		if(f48_ij % 2 != 0)
//			error_counter++;
		f48_i = f48_i + (f48_ij/2);
		f33_i = f33_i + f33_uij + f33_vij;

		// j in N_u (N_ui_bar)
		vector<NodeID_TYPE> N_ui_bar = set_difference(N_u,N_u_key[i]);
		Count_TYPE f26_uij=0,f26_vij=0,f19_ij=0;
		Count_TYPE f44_ij=0;
		for(int idx1 = 0; idx1 < N_ui_bar.size(); idx1++)
		{
			NodeID_TYPE j = N_ui_bar[idx1];
			// k in N_u
			vector<NodeID_TYPE> N_uij = intersection(N_u_key[i],N_u_key[j]);
			f26_uij += N_u.size() - N_u_key[i].size() - N_u_key[j].size() + N_uij.size() -1;
			// k in N_v
			vector<NodeID_TYPE> N_vij = intersection(N_v_key[i],N_v_key[j]);
			f44_ij += N_v_key[j].size() - N_vij.size();
			f19_ij += N_v.size() - N_v_key[i].size() - N_v_key[j].size() + N_vij.size();
		}
//		if(f26_uij % 2 != 0)
//			error_counter++;
		f26_i = f26_i + (f26_uij/2);
		f19_i = f19_i + f19_ij;
		f44_i = f44_i + f44_ij;
		// j in N_v (N_vi_bar)
		vector<NodeID_TYPE> N_vi_bar = set_difference(N_v,N_v_key[i]);
		for(int idx1 = 0; idx1 < N_vi_bar.size(); idx1++)
		{
			NodeID_TYPE j = N_vi_bar[idx1];
			// k in N_v
			vector<NodeID_TYPE> N_vij = intersection(N_v_key[i],N_v_key[j]);
			f26_vij += N_v.size() - N_v_key[i].size() - N_v_key[j].size() + N_vij.size() -1;
		}
//		if(f26_vij % 2 != 0)
//			error_counter++;
		f26_i = f26_i + (f26_vij/2);

	//algo2   j in N_u
//		Count_TYPE f65_ij_u=0,f64_ij_u=0,f61_ij_u=0,f54_ij_u=0;
	//algo3  j in N_u
//		Count_TYPE f59_ij_u=0,f52_ij_u=0,f47_ij_u=0,f34_ij_u=0;
		Count_TYPE f63_ij_u=0,f56_ij_u=0,f55_ij_u=0,f40_ij_u=0;
		for(int idx1 = 0; idx1 < N_u_key[i].size(); idx1++)
		{
			NodeID_TYPE j = N_u_key[i][idx1];
			// algo 2 *code removed*
			// algo3
			// k in N_u
//			vector<NodeID_TYPE> N_uij = intersection(N_u_key[i],N_u_key[j]);
//			f59_ij_u += N_uij.size();
//			f52_ij_u += N_u_key[j].size() - N_uij.size();
//			f47_ij_u += N_u_key[i].size() - N_uij.size() - 1;
//			f34_ij_u += N_u.size() - N_u_key[i].size() - N_u_key[j].size() + N_uij.size();
			// k in N_v
			vector<NodeID_TYPE> N_vij = intersection(N_v_key[i],N_v_key[j]);
			f63_ij_u += N_vij.size();
			f56_ij_u += N_v_key[j].size() - N_vij.size();
			f55_ij_u += N_v_key[i].size() - N_vij.size();
			f40_ij_u += N_v.size() - N_v_key[i].size() - N_v_key[j].size() + N_vij.size();


		}

		f63_i = f63_i + f63_ij_u;
		f56_i = f56_i + f56_ij_u;
		f55_i = f55_i + f55_ij_u;
		f40_i = f40_i + f40_ij_u;

	//algo2   j in N_v
//		Count_TYPE f65_ij_v=0,f64_ij_v=0,f61_ij_v=0,f54_ij_v=0;
	//algo3  j in N_v
//		Count_TYPE f59_ij_v=0,f52_ij_v=0,f47_ij_v=0,f34_ij_v=0;
		Count_TYPE f56_ij_v=0,f40_ij_v=0;
		for(int idx1 = 0; idx1 < N_v_key[i].size(); idx1++)
		{
			NodeID_TYPE j = N_v_key[i][idx1];
			// algo 2 *code removed*
			// algo3
			// k in N_v
//			vector<NodeID_TYPE> N_vij = intersection(N_v_key[i],N_v_key[j]);
//			f59_ij_v += N_vij.size();
//			f52_ij_v += N_v_key[j].size() - N_vij.size();
//			f47_ij_v += N_v_key[i].size() - N_vij.size() - 1;
//			f34_ij_v += N_v.size() - N_v_key[i].size() - N_v_key[j].size() + N_vij.size();
			// k in N_u
			vector<NodeID_TYPE> N_uij = intersection(N_u_key[i],N_u_key[j]);
			f56_ij_v += N_u_key[j].size() - N_uij.size();
			f40_ij_v += N_u.size() - N_u_key[i].size() - N_u_key[j].size() + N_uij.size();

		}
		f56_i = f56_i + f56_ij_v;
		f40_i = f40_i + f40_ij_v;
	}

//----------------------------------

	freq[45] = f67_i;
	freq[44] = f66_i/2;
	freq[39] = f60_i;
	freq[31] = f50_i;
	//algo6
	freq[30] = f48_i/3;
	freq[21] = f33_i/2;
	freq[17] = f26_i;
	freq[15] = f19_i;
	freq[27] = f44_i;
	//algo2
//	freq[43] = f65_i/2;
//	freq[42] = f64_i/2;
//	freq[40] = f61_i;
//	freq[34] = f54_i;
	//algo3
//	freq[38] = f59_i;
//	freq[33] = f52_i;
//	freq[29] = f47_i;
//	freq[22] = f34_i;
	freq[41] = f63_i;
	freq[36] = f56_i;
	freq[35] = f55_i;
	freq[25] = f40_i;

}


void algorithm457_unique(NodeID_TYPE u, NodeID_TYPE v,vector<NodeID_TYPE> &T,vector<NodeID_TYPE> &N_u,vector<NodeID_TYPE> &N_v,unordered_map<NodeID_TYPE,vector<NodeID_TYPE> > &T_key,unordered_map<NodeID_TYPE,vector<NodeID_TYPE> > &N_u_key,unordered_map<NodeID_TYPE,vector<NodeID_TYPE> > &N_v_key, vector<Count_TYPE> &freq)
{
	//algo4
//	Count_TYPE f51_i=0,f35_i=0,f27_i=0,f57_i=0,f45_i=0,f23_i=0,f37_i=0;
	Count_TYPE f23_i=0,f37_i=0;
	//algo5
	Count_TYPE f42_i=0,f30_i=0,f17_i=0,f15_i=0;
	int error_counter = 0 ;
//i in N_u
	for(int idx =0; idx < N_u.size();idx++)
	{
	// algo4  j in N_u
		NodeID_TYPE i = N_u[idx];
//		Count_TYPE f51_ij=0,f35_ij=0,f27_ij=0,f57_ij=0,f45_ij=0,f23_ij=0,f37_ij=0;
		Count_TYPE f23_ij=0,f37_ij=0;
		for(int idx1 = 0; idx1 < N_u_key[i].size(); idx1++)
		{
			NodeID_TYPE j = N_u_key[i][idx1];
			if(j < i)
			{
//				vector<NodeID_TYPE> N_uij = intersection(N_u_key[i],N_u_key[j]);
//				f35_ij += N_u_key[j].size() - N_uij.size() - 1;
//				vector<NodeID_TYPE> N_vij = intersection(N_v_key[i],N_v_key[j]);
//				f45_ij += N_v_key[j].size() - N_vij.size();
				continue;
			}
			// k in N_u
//			int inter_size;
//			vector<NodeID_TYPE> N_uij = intersection(N_u_key[i],N_u_key[j],j,inter_size);
//			f51_ij += inter_size;
//			f35_ij += N_u_key[j].size() - N_uij.size() - 1;
//			f27_ij += N_u.size() - N_u_key[i].size() - N_u_key[j].size() + N_uij.size();

			// k in N_v
			vector<NodeID_TYPE> N_vij = intersection(N_v_key[i],N_v_key[j]);
//			f57_ij += N_vij.size();
//			f45_ij += N_v_key[j].size() - N_vij.size();
			f23_ij += N_v.size() - N_v_key[i].size() - N_v_key[j].size() + N_vij.size();
			// k in T
			vector<NodeID_TYPE> N_Tij = intersection(T_key[i],T_key[j]);
			f37_ij += T.size() - T_key[i].size() - T_key[j].size() + N_Tij.size();
		}
		f23_i = f23_i + f23_ij;
		f37_i = f37_i + f37_ij;

	//algo5   j in N_u (N_ui_bar)
		Count_TYPE f42_ij=0,f30_ij=0;
		Count_TYPE f17_ij=0,f15_ij=0;
		vector<NodeID_TYPE> temp_N_u;
		for(int k = 0 ;k < N_u.size();k++)
		{
			if(N_u[k] != i)
				temp_N_u.push_back(N_u[k]); 
		}
		vector<NodeID_TYPE> N_ui_bar = set_difference(temp_N_u,N_u_key[i]);
		for(int idx1 = 0; idx1 < N_ui_bar.size(); idx1++)
		{
			NodeID_TYPE j = N_ui_bar[idx1];
			// k in N_u
			vector<NodeID_TYPE> N_uij = intersection(N_u_key[i],N_u_key[j]);
			f17_ij += N_u.size() - N_u_key[i].size() - N_u_key[j].size() + N_uij.size() - 2;
			// k in N_v
			vector<NodeID_TYPE> N_vij = intersection(N_v_key[i],N_v_key[j]);
			f42_ij += N_vij.size();
			f30_ij += N_v_key[j].size() - N_vij.size();
			f15_ij += N_v.size() - N_v_key[i].size() - N_v_key[j].size() + N_vij.size();
		}
		f17_i = f17_i + (f17_ij/2);
		f15_i = f15_i + f15_ij;
		f42_i = f42_i + f42_ij;
		f30_i = f30_i + f30_ij;
	}
//i in N_v
	for(int idx =0; idx < N_v.size();idx++)
	{
	// algo4  j in N_u
		NodeID_TYPE i = N_v[idx];
//		Count_TYPE f51_ij=0,f35_ij=0,f27_ij=0,f57_ij=0,f45_ij=0,f23_ij=0,f37_ij=0;
		Count_TYPE f23_ij=0,f37_ij=0;
		for(int idx1 = 0; idx1 < N_v_key[i].size(); idx1++)
		{
			NodeID_TYPE j = N_v_key[i][idx1];
			if(j < i)
			{
//				vector<NodeID_TYPE> N_vij = intersection(N_v_key[i],N_v_key[j]);
//				f35_ij += N_v_key[j].size() - N_vij.size() - 1;
//				vector<NodeID_TYPE> N_uij = intersection(N_u_key[i],N_u_key[j]);
//				f45_ij += N_u_key[j].size() - N_uij.size();
				continue;
			}
			// k in N_v
			int inter_size;
//			vector<NodeID_TYPE> N_vij = intersection(N_v_key[i],N_v_key[j],j,inter_size);
//			f51_ij += inter_size;
//			f35_ij += N_v_key[j].size() - N_vij.size() - 1;
//			f27_ij += N_v.size() - N_v_key[i].size() - N_v_key[j].size() + N_vij.size();

			// k in N_u
			vector<NodeID_TYPE> N_uij = intersection(N_u_key[i],N_u_key[j]);
//			f57_ij += N_uij.size();
//			f45_ij += N_u_key[j].size() - N_uij.size();
			f23_ij += N_u.size() - N_u_key[i].size() - N_u_key[j].size() + N_uij.size();

			// k in T
			vector<NodeID_TYPE> N_Tij = intersection(T_key[i],T_key[j]);
			f37_ij += T.size() - T_key[i].size() - T_key[j].size() + N_Tij.size();
		}
		f23_i = f23_i + f23_ij;
		f37_i = f37_i + f37_ij;

	//algo5   j in N_v (N_vi_bar)
		Count_TYPE f42_ij=0,f30_ij=0;
		Count_TYPE f17_ij=0,f15_ij=0;
		vector<NodeID_TYPE> temp_N_v;
		for(int k = 0 ;k < N_v.size();k++)
		{
			if(N_v[k] != i)
				temp_N_v.push_back(N_v[k]); 
		}
		vector<NodeID_TYPE> N_vi_bar = set_difference(temp_N_v,N_v_key[i]);
		for(int idx1 = 0; idx1 < N_vi_bar.size(); idx1++)
		{
			NodeID_TYPE j = N_vi_bar[idx1];
			// k in N_v
			vector<NodeID_TYPE> N_vij = intersection(N_v_key[i],N_v_key[j]);
			f17_ij += N_v.size() - N_v_key[i].size() - N_v_key[j].size() + N_vij.size() - 2;
			// k in N_u
			vector<NodeID_TYPE> N_uij = intersection(N_u_key[i],N_u_key[j]);
			f42_ij += N_uij.size();
			f30_ij += N_u_key[j].size() - N_uij.size();
			f15_ij += N_u.size() - N_u_key[i].size() - N_u_key[j].size() + N_uij.size();
		}
		f17_i = f17_i + (f17_ij/2);
		f15_i = f15_i + f15_ij;
		f42_i = f42_i + f42_ij;
		f30_i = f30_i + f30_ij;
	}
	freq[16] = f23_i;
	freq[24] = f37_i;

	//algo5
	freq[14] = f17_i/3;
	freq[13] = f15_i/2;
	freq[26] = f42_i/2;
	freq[20] = f30_i;

}


