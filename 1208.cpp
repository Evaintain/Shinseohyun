#include <iostream>
#include <map>
#include <vector>
#include <algorithm>

using namespace std;

/*
1208번 문제 접근 방식
->
수열을 2개로 나눠서 한쪽은 갯수를 정리하고 나머지 한쪽은 경우의수를 구해서 구한다.
틀린이유 : 2^40 - 1까지 가능한데 2^31 - 1 까지 가능한 int 써서 틀림
왼쪽, 오른쪽 둘다 goal과 같을때 세었는데, 오른쪽만 세어도 된다.
*/

/*
태그
. 이분 탐색
. 중간에서 만나기
*/

int arr[47];

class array_control
{
private:
    vector<int> left;
    vector<int> right;
    map<int, int> set_right;
    int sum = 0;
    long long cnt = 0;

public:
    void make_left_arr(int start, int mid, int goal)
    {
        for (int i = 1; i < (1 << mid); i++)
        {
            sum = 0;
            for (int j = 0; j < mid; j++)
            {
                if (i & (1 << j))
                {
                    sum += arr[j];
                }
            }

            left.push_back(sum);
        }
        sort(left.begin(), left.end());
    }

    void make_right_arr(int mid, int _end, int goal)
    {
        for (int i = 1; i < (1 << _end - mid); i++)
        {
            sum = 0;
            for (int j = 0; j < _end - mid; j++)
            {
                if (i & (1 << j))
                {
                    sum += arr[mid + j];
                }
            }

            if (sum == goal)
            {
                cnt++;
            }

            right.push_back(sum);
        }

        sort(right.begin(), right.end());
    }

    void make_set()
    {
        int idx = 0;
        for (int i = 0; i < right.size(); i = i + idx)
        {
            idx = upper_bound(right.begin(), right.end(), right[i]) - lower_bound(right.begin(), right.end(), right[i]);
            set_right[right[i]] = idx;
        }
    }

    void counting_num(int goal)
    {
        for (int i = 0; i < left.size(); i++)
        {
            if (left[i] == goal)
            {
                cnt++;
            }

            cnt += set_right[goal - left[i]];
        }
    }

    void print()
    {
        printf("%lld", cnt);
    }
};

int main()
{
    array_control ac;

    int n;
    int s;
    scanf("%d %d", &n, &s);
    for (int i = 0; i < n; i++)
    {
        scanf("%d", &arr[i]);
    }

    ac.make_left_arr(0, n/2, s);
    ac.make_right_arr(n/2, n, s);
    ac.make_set();
    ac.counting_num(s);
    ac.print();
}
