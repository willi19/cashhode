#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
#define all(v) (v).begin(),(v).end()
const ll INF=1e15;
int N;
ll tsp[16][1<<16];
ll w[16][16];
int main(){
    scanf("%d",&N);
    for(int i=0;i<N;i++)
        for(int j=0;j<N;j++)
            {scanf("%lld",&w[i][j]);
            }
    for(int i=0;i<N;i++)
        fill(tsp[i],tsp[i]+(1<<N),INF);
    tsp[0][1]=0;
    for(int b=1;b<(1<<N)-1;b++){
        for(int i=0;i<N;i++){
            if(!(b&1<<i)) continue;
            for(int j=0;j<N;j++){
                if(!w[i][j] || (b&1<<j)) continue;
                tsp[j][b|1<<j]=
                min(tsp[j][b|1<<j],tsp[i][b]+w[i][j]);
            }
        }
    }
    ll small=INF;
    for(int i=1;i<N;i++)
    {
        if(small>tsp[i][(1<<N)-1]+w[i][0]&&w[i][0]!=0)
            small=tsp[i][(1<<N)-1]+w[i][0];
    }
    printf("%lld",small);
}

typedef vector<vector<int>> vvi;

int interest_score(vector<int> &A, vector<int> &B){
    vector<int> resultU;
    merge(all(A), all(B), back_inserter(resultU));
    resultU.erase(unique(all(resultU)), resultU.end());
    int Union_size = resultU.size();
    //cout<<"Union_size = "<<Union_size<<"\n";
    int a = Union_size-A.size();
    int b = Union_size-B.size();
    int c = A.size()+B.size()-Union_size;
    return min(a, min(b, c));
}

int main(){
    pcvvi input = LOAD::load("data\\e.txt");
    vector<char> oreint = input.first;
    vvi orig_tag_list = input.second;
    for(int i=0 ; i<orig_tag_list.size() ; i++) sort(orig_tag_list[i].begin(), orig_tag_list[i].end());
    vvi tag_list;
    int N;
    ifstream cinf;
    cinf.open("b_greedy.txt");
    cinf>>N;
    for(int i=0;i<N;i++)
    {
        int a,b;
        cinf>>a;
        if(oreint[a] == 'V')
        {
            cinf>>b;
            tag_list.push_back(sum_list(orig_tag_list[a],orig_tag_list[b]));
        }
        else tag_list.push_back(orig_tag_list[a]);
    }


    cinf.close();
}