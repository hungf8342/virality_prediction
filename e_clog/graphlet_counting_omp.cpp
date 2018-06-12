#include "size4_counting_preProcessing.cpp"
#include "size5_graphlet_counting.cpp"

#ifdef _OPENMP
#  include <omp.h>
#else
int omp_get_max_threads()       { return 1; }
void omp_set_num_threads(int)   {}
int omp_get_thread_num()        { return 0; }
#endif

using namespace std;

Runtimecounter rt1,rt2;
graph g;
vector<pair<NodeID_TYPE,NodeID_TYPE> > edge_list;
int num_threads = -1;
int is_all = 0, is_local = 1, is_unique = 0, edge_file = 0;

inline bool myfunction(pair<NodeID_TYPE,NodeID_TYPE> a,pair<NodeID_TYPE,NodeID_TYPE> b){return (a.second > b.second);}

double readFile(FILE * &input,int has_edge_att)
{
	rt1.start();
	NodeID_TYPE T;
	if(has_edge_att == 1)
		int tt = fscanf(input,"%u%u%u",&N,&M,&T);
	else
		int tt = fscanf(input,"%u%u",&N,&M);

	NodeID_TYPE u , v, t;
	NodeID_TYPE count = 0;
	unordered_map<NodeID_TYPE,unordered_map<NodeID_TYPE,int> > map;
//	vector<NodeID_TYPE> local_nodes;
	// reading the file
    	for(NodeID_TYPE i=0;i<M;i++)
	{
		if(has_edge_att == 1)
			int tt = fscanf(input,"%u%u%u",&u,&v,&t );
		else
			int tt = fscanf(input,"%u%u",&u,&v);

		if(u == v)
			continue;

		auto it = map.find(u);
		if(it != map.end())
		{
			auto it1 = it->second.find(v);
			if(it1 != it->second.end())
			{
//				cout << "duplicate edge: " << u << "-" << v << endl;
				continue;
			}
			else
			{
				it->second[v]  = 1;
			}
		}
		else
		{
			//local_nodes.push_back(u);
			unordered_map<NodeID_TYPE,int> m;
			m[v] = 1;
			map[u] = m;
		}
		auto it1 = map.find(v);
		if(it1 != map.end())
		{
			auto it11 = it1->second.find(u);
			if(it11 != it1->second.end())
			{
//				cout << "duplicate edge: " << u << "-" << v << endl;
				continue;
			}
			else
			{
				it1->second[u]  = 1;
			}
		}
		else
		{
			//local_nodes.push_back(v);
			unordered_map<NodeID_TYPE,int> m;
			m[u] = 1;
			map[v] = m;
		}
		if(u < v)
			edge_list.push_back(make_pair(u,v));
		else
			edge_list.push_back(make_pair(v,u));
		count++;
   	}
	fclose(input);
	rt1.stop();
	double read_time = rt1.GetRuntime();

	if(count != M)
		M = count;

	g.init_graph(N,M);

	return read_time;
}
double read_edgefile(FILE * &edgefile)
{
// change the edge_list variable

	unsigned int num;
	int tt = fscanf(edgefile,"%u",&num);

	NodeID_TYPE u , v;
	vector<pair<NodeID_TYPE,NodeID_TYPE> > new_edge_list;
	// read edges
    	for(unsigned int i=0; i < num; i++)
	{
		int tt = fscanf(edgefile,"%u%u",&u,&v);
		new_edge_list.push_back(make_pair(u,v));
	}

	edge_list = new_edge_list;
	rt1.stop();
	double edge_read_time = rt1.GetRuntime();
	return edge_read_time;

}
double sort_edgeList()
{
	rt1.start();
	cout << "sorting started\n" << std::flush;
	vector< pair<NodeID_TYPE,NodeID_TYPE> > idx_degree;
	for(NodeID_TYPE i = 0; i < edge_list.size(); i++)
	{
		NodeID_TYPE deg_sum = g.get_edge_degreeSum(edge_list[i]);
		idx_degree.push_back(make_pair(i,deg_sum));
	}
	cout << "index sorted\n"<< std::flush;
	sort(idx_degree.begin(),idx_degree.end(),myfunction);
	vector<pair<NodeID_TYPE,NodeID_TYPE> > new_edge_list;
	for(NodeID_TYPE i = 0; i < idx_degree.size(); i++)
	{
		new_edge_list.push_back(edge_list[idx_degree[i].first]);
	}
//	for(NodeID_TYPE i = 0; i < idx_degree.size(); i++)
//	{
//		cout << g.get_edge_degreeSum(new_edge_list[i]) << " : ";
//	}

	cout << "edge sorted\n"<< std::flush;

	edge_list = new_edge_list;
	rt1.stop();
	double sort_time = rt1.GetRuntime();
	return sort_time;
}
double get_graphlet_freqency_matrix(char* label_name1,char* label_name2)
{
	int edge_size = edge_list.size();
	vector<vector<Count_TYPE> > mat (edge_size);
//	vector<double> time_list (edge_size);
	int max_t = omp_get_max_threads();
	if(num_threads <= 0)
		omp_set_num_threads(max_t);
	else
		omp_set_num_threads(num_threads);

	int n_thrd = omp_get_max_threads();

	if(is_local == 1)
	{
		rt1.start();
		#pragma omp parallel for schedule(dynamic)
		for(NodeID_TYPE i = 0; i < edge_size; i++)
		{
			unordered_map<NodeID_TYPE,vector<NodeID_TYPE> > T_key,N_u_key,N_v_key;
			vector<NodeID_TYPE> T,N_u,N_v;
			vector<int> status_map (N,0);
//			rt2.start();
			vector<Count_TYPE> freq_vector = get_freqency_vector(edge_list[i].first,edge_list[i].second,g,T,N_u,N_v,T_key,N_u_key,N_v_key,status_map);
			algorithm1236(edge_list[i].first,edge_list[i].second,T,N_u,N_v,T_key,N_u_key,N_v_key,freq_vector);
			algorithm457(edge_list[i].first,edge_list[i].second,T,N_u,N_v,T_key,N_u_key,N_v_key,freq_vector);
//			rt2.stop();
		
//			time_list[i] = rt2.GetRuntime();
			mat[i] = freq_vector;

		}

		rt1.stop();
	}
	else if(is_all == 1)
	{
		rt1.start();
		#pragma omp parallel for schedule(dynamic)
		for(NodeID_TYPE i = 0; i < edge_size; i++)
		{
			unordered_map<NodeID_TYPE,vector<NodeID_TYPE> > T_key,N_u_key,N_v_key;
			vector<NodeID_TYPE> T,N_u,N_v;
			vector<int> status_map (N,0);
//			rt2.start();
			vector<Count_TYPE> freq_vector = get_freqency_vector(edge_list[i].first,edge_list[i].second,g,T,N_u,N_v,T_key,N_u_key,N_v_key,status_map);
			size5_path_cycle(edge_list[i].first,edge_list[i].second,g,T,N_u,N_v,T_key,N_u_key,N_v_key,freq_vector, status_map);
			algorithm1236(edge_list[i].first,edge_list[i].second,T,N_u,N_v,T_key,N_u_key,N_v_key,freq_vector);
			algorithm457(edge_list[i].first,edge_list[i].second,T,N_u,N_v,T_key,N_u_key,N_v_key,freq_vector);
//			rt2.stop();
		
//			time_list[i] = rt2.GetRuntime();
			mat[i] = freq_vector;

		}

		rt1.stop();
	}
	else if(is_unique == 1)
	{
		rt1.start();
		rt2.start();
		#pragma omp parallel for schedule(dynamic)
		for(NodeID_TYPE i = 0; i < edge_size; i++)
		{
			unordered_map<NodeID_TYPE,vector<NodeID_TYPE> > T_key,N_u_key,N_v_key;
			vector<NodeID_TYPE> T,N_u,N_v;
			vector<int> status_map (N,0);

			vector<Count_TYPE> freq_vector = get_freqency_vector(edge_list[i].first,edge_list[i].second,g,T,N_u,N_v,T_key,N_u_key,N_v_key,status_map);
			size5_path_cycle(edge_list[i].first,edge_list[i].second,g,T,N_u,N_v,T_key,N_u_key,N_v_key,freq_vector, status_map);
			algorithm1236_unique(edge_list[i].first,edge_list[i].second,T,N_u,N_v,T_key,N_u_key,N_v_key,freq_vector);
			algorithm457_unique(edge_list[i].first,edge_list[i].second,T,N_u,N_v,T_key,N_u_key,N_v_key,freq_vector);
			mat[i] = freq_vector;

//			if(i%1000==0)
//			{
//				rt2.stop();
//				cout << "cur edge degree sum" << g.get_edge_degreeSum(edge_list[i]) << "\tEdges processed: " << i << "\t time taken: " << rt2.GetRuntime() << " sec" << endl;
//				rt2.start();
//			}

		}

		rt1.stop();
	}
	double count_time = rt1.GetRuntime();
	cout << "Max # threads: "<< max_t <<endl;
	cout << "# threads approved: "<< n_thrd <<endl;
	cout << "freq counting time: "<< count_time << "sec" <<endl;
	cout.flush();

//*
	rt1.start();
	FILE *fo = fopen(label_name1, "wb");
	for(NodeID_TYPE i = 0; i < edge_list.size(); i++)
//	for(NodeID_TYPE i = 0; i < 2; i++)
	{
		fprintf(fo,"%u %u:",edge_list[i].first,edge_list[i].second);
		for (int a = 0; a < graphlet_count; a++) 
			fprintf(fo, " %llu", mat[i][a]);
		fprintf(fo, "\n");
	}
	fclose(fo);
/*
	FILE *fo1 = fopen(label_name2, "wb");
	for(NodeID_TYPE i = 0; i < edge_list.size(); i++)
//	for(NodeID_TYPE i = 0; i < 2; i++)
	{
		NodeID_TYPE u = edge_list[i].first;
		NodeID_TYPE v = edge_list[i].second;
		fprintf(fo1,"%u %u",u,v);
		fprintf(fo1," %d %d %lf",nei_size[u],nei_size[v],time_list[i]);
		fprintf(fo1, "\n");
	}

	fclose(fo1);
//*/
	rt1.stop();
	double count_time1 = rt1.GetRuntime();
//*/
	cout << "write time: "<< count_time1 << "sec" <<endl;
	cout.flush();
	return count_time;
}
int main(int argc, char **argv)
{
 
	// read args
	if (argc == 1) {
//		usage();
		cout << "Enter filename..."<<endl;
		return 1;
	}
	int i = 1, has_edge_att = 0;
	char *filename,*edge_filename; //,*filename1,*resfilename,*queryfile; // *resfilename="../index/"
	while (i < argc) {
/*		if (strcmp("-h", argv[i]) == 0) {
			usage();
			return 1;
		}
//*/
		if (strcmp("-i", argv[i]) == 0) {
			i++;
			filename = argv[i++];
			continue;
		}
		if (strcmp("-edgefile", argv[i]) == 0) {
			i++;
			edge_file = 1;
			edge_filename = argv[i++];
			continue;
		}
		if (strcmp("-EdgeAtt", argv[i]) == 0) {
			i++;
			has_edge_att = 1;
			continue;
		}
		if (strcmp("-t", argv[i]) == 0) {
			i++;
			num_threads = atoi(argv[i++]);
			continue;
		}
		if (strcmp("-all", argv[i]) == 0) {
			i++;
			is_all = 1;
			is_local = 0;
			is_unique = 0;
			continue;
		}
		if (strcmp("-local", argv[i]) == 0) {
			i++;
			is_all = 0;
			is_local = 1;
			is_unique = 0;
			continue;
		}
		if (strcmp("-unique", argv[i]) == 0) {
			i++;
			is_all = 0;
			is_local = 0;
			is_unique = 1;
			continue;
		}


	}
	FILE *in_file = fopen(filename, "r");		// graph input file
	int idx=0;
	char label_name1[200];

	if(edge_file == 1)
	{
		for(char *i=edge_filename; *i != '\0'; i++){
				label_name1[idx++]=*i;
		}
	}
	else
	{
		for(char *i=filename; *i != '\0'; i++){
				label_name1[idx++]=*i;
		}
	}
	if(is_all == 1)
	{
		char mid[6] = "_all";
		for(char *i=mid; *i != '\0'; i++){
				label_name1[idx++]=*i;
		}
	}
	else if(is_local == 1)
	{
		char mid[10] = "_local";
		for(char *i=mid; *i != '\0'; i++){
				label_name1[idx++]=*i;
		}
	}
	else if(is_unique == 1)
	{
		char mid[10] = "_unique";
		for(char *i=mid; *i != '\0'; i++){
				label_name1[idx++]=*i;
		}
	}
	char hop_lbl[30] = "_graphlet_freqeuncy_5_omp.txt";
	for(char *i=hop_lbl; *i != '\0'; i++){
			label_name1[idx++]=*i;
	}
	label_name1[idx++]='\0';
	idx=0;

	char label_name2[80];
/*
	for(char *i=filename; *i != '\0'; i++){
			label_name2[idx++]=*i;
	}
	char hop_lbl1[25] = "_timings_omp.txt";
	for(char *i=hop_lbl1; *i != '\0'; i++){
			label_name2[idx++]=*i;
	}
	label_name2[idx++]='\0';
//*/
	double read_time;
	read_time = readFile(in_file,has_edge_att);
	cout << "read time: "<< read_time << "sec" <<endl;
	cout.flush();

	double adj_list_time = g.make_adjList(edge_list);	
	cout << "Create Adj list time: "<< adj_list_time << "sec" <<endl;
	cout.flush();

	double sort_edge_time = g.sort_edges();
	cout << "edge sorting time: "<< sort_edge_time << "sec" <<endl;
	cout.flush();

//	disp_edges(0);

	double edge_convert_time = g.convert_to_sparse();
	cout << "edge conversion time: "<< edge_convert_time << "sec" <<endl;
	cout.flush();
//	disp_edges(1);

	if(edge_file == 1)
	{
		FILE *edgefile = fopen(edge_filename, "r");
		double edgelist_read_time = read_edgefile(edgefile);
		cout << "Edgelist read time: "<< edgelist_read_time << "sec" <<endl;

	}

	// sort the edge_list
	double edgeList_sort_time = sort_edgeList();
	cout << "edge sorting time: "<< edgeList_sort_time << "sec" <<endl;
	cout.flush();

	double count4_time = get_graphlet_freqency_matrix(label_name1,label_name2);


    return 0;
}
