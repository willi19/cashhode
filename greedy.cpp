#define all(v) (v).begin(),(v).end()
#include <iostream>
#include <vector>
#include <algorithm>
#include <iomanip>
#include <fstream>
#include <string>
#include <unordered_map>
#include "load.cpp"
using namespace std;
const int MAXN = 100005;
bool compare(int i, int j) { return i > j; }
typedef vector<vector<int>> vvi;
typedef pair<vvi, vvi> pvvvv;
typedef pair<vector<char>, vector<vector<int>>> pcvvi;

pvvvv gen_sorted_Slides(vector<int> V, vector<int> H, vector<vector<int>> tags){
    vector<vector<int>> tags_in_Slides;
    vector<vector<int>> images_in_Slides;
    // descending order sorting
    sort(V.begin(), V.end(),[&](int i, int j){return tags[i].size() > tags[j].size();});
    for(int i : H){
        vector<int> image_idx;
        image_idx.push_back(i);
        images_in_Slides.push_back(image_idx);
        tags_in_Slides.push_back(tags[i]);
    }
    for(int i=0 ; i<V.size()/2 ; i++){
        vector<int> Slide;
        merge(all(tags[V[i]]), all(tags[V[i+1]]), back_inserter(Slide));
        Slide.erase(unique(all(Slide)), Slide.end());
        tags_in_Slides.push_back(Slide);
        vector<int> image_idx;
        image_idx.push_back(V[i]);
        image_idx.push_back(V[i+1]);
        images_in_Slides.push_back(image_idx);
    }

    return pvvvv(tags_in_Slides, images_in_Slides);
}

//calculate interest between tags A, B
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
vvi greedy_select(vector<char> orient,  vector<vector<int>> tags){
    vector<int> V, H;
    for(int i=0 ; i<tags.size() ; i++){
        if(orient[i] == 'V'){
            V.push_back(i);
        }
        else if(orient[i] == 'H'){
            H.push_back(i);
        }
        else{
            cout<<"orient[i] neither V, H\n";
            return vvi();
        }
    }
    for(int i=0 ; i<tags.size() ; i++) sort(tags[i].begin(), tags[i].end());

    pvvvv sorted_Slides = gen_sorted_Slides(V, H, tags);
    vvi tags_in_Slides = sorted_Slides.first;
    for (int i=0 ; i<tags_in_Slides.size() ; i++){
        sort(all(tags_in_Slides[i]));
    }
    vvi images_in_Slides = sorted_Slides.second;

    vector<int> Slide_show;
    int ck[MAXN];
    for(int i=0 ; Slide_show.size() ; i++){
        ck[i] = 0;
    }

    //set start index = 0
    int s_idx = 0;
    Slide_show.push_back(s_idx);
    ck[s_idx] = 1;

    //find greedy idx
    int tot_score = 0;
    while(Slide_show.size() < tags_in_Slides.size()){
        //cout<<Slide_show.size()<<"\n";
        int i = Slide_show[Slide_show.size() - 1];
        int idx=-1, max_score=-1;
        int it = 0;
        for(int j=0 ; j<tags_in_Slides.size() ; j++){
            if(ck[j]) continue;
            it++;
            if(it>100)break;
            int score = interest_score(tags_in_Slides[i], tags_in_Slides[j]);
            //cout<<"i, j, score = "<<i<<" "<<j<<" "<<score<<"\n";
            if(score > max_score){
                max_score = score;
                idx = j;
            }
        }
        tot_score += max_score;
        Slide_show.push_back(idx);
        ck[idx] = 1;
    }
    /*cout<<"Slide show = \n";
    for(int i : Slide_show){
        cout<<i<<" ";
    }
    cout<<"\n";
    cout<<"Images_in_Slide = \n";
    for(auto A : images_in_Slides){
        for(int i:A){
            cout<<i<<" ";
        }
        cout<<"\n";
    }
    cout<<"tags_in_Slide = \n";
    for(auto A : tags_in_Slides){
        for(int i:A){
            cout<<i<<" ";
        }
        cout<<"\n";
    }
    cout<<"\n";*/
    vvi results;
    for(int i=0 ; i<Slide_show.size() ; i++){
        results.push_back(images_in_Slides[Slide_show[i]]);
    }
    cout<<"greedy_score = "<<tot_score<<"\n";
    return results;
}
int main(){
    pcvvi input = LOAD::load("data\\b.txt");
    vector<char> orient = input.first;
    vvi tags = input.second;
    /*cout<<"tags\n";
    for(auto A:tags){
        for(int i:A){
            cout<<i<<" ";
        }
        cout<<"\n";
    }
    for(char a:orient){
        cout<<a<<" ";
    }
    cout<<"\n";
    cout<<"\n";*/
    vvi results = greedy_select(orient,  tags);
    LOAD::save_results(results, "output\\b_greedy.txt");
    cout<<"\n\n";
    /*
    for(auto A : results){
        for(int i: A){
            cout<<i<<" ";
        }
        cout<<"\n";
    }*/

}