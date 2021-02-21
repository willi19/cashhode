
#include <iostream>
#include <iomanip>
#include <fstream>
#include <vector>
#include <string>
#include <unordered_map>

namespace LOAD{
    using namespace std;
    typedef vector<vector<int>> vvi;
    typedef pair<vector<char>, vvi> pcvvi;
    pcvvi load(string data_path) {
        int x;
        unordered_map<string, int> um;
        ifstream cinf;
        
        cinf.open(data_path);
        if (!cinf) {
            cout << "Unable to open file";
            exit(1); // terminate with error
        }
        int N;
        cinf>>N;
        vector<char> orient;
        vector<vector<int>> tags;
        for(int i=0, m ; i<N ; i++){
            char c;
            cinf>>c;
            cinf>>m;
            vector<int> tag;
            for(int j=0 ; j<m ; j++){
                string S;
                cinf>>S;
                if(um.find(S) == um.end()){
                    um.insert(make_pair(S, um.size()));
                }
                int x = um[S];
                tag.push_back(x);
            }
            tags.push_back(tag);
            orient.push_back(c);
        }
        cinf.close();
        return pcvvi(orient, tags);
    }
    void save_results(vvi results, string save_path){
        ofstream outFile(save_path);
        outFile << results.size()<<"\n";
        for(auto A : results){
            for(int i:A){
                outFile<<i<<" ";
            }
            outFile<<"\n";
        }
        outFile.close();
    }
}