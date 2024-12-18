"""
Problem Link: https://leetcode.com/problems/candy/description/
This solution, which has time complexity of O(nlogn), is slightly worse than the optimal solution, which has time complexity of O(n)
"""

class Solution:
    def candy(self, ratings: List[int]) -> int:
        # 1. Create empty arr to store no of candies allocated to each child
        ratings_len = len(ratings)
        candy_alloc = [0 for _ in range(ratings_len + 2)]
        # first and last element in candy_alloc stores nothing, is always 0

        # 2. Linear scan through arr and throw position in hash table, O(n)
        rating_posn = {}
        unique_ratings = []
        index = 0
        for rating in ratings:
            if rating not in rating_posn:
                rating_posn[rating] = [index]
                unique_ratings += [rating]
            else:
                rating_posn[rating] += [index]
            index += 1

        # 3. Sort the unique ratings, O(nlogn)
        unique_ratings.sort()

        ratings = [-1] + ratings + [-1]

        # 4. Allocate candies to each child, starting with lower ratings
        for unique in unique_ratings:
            posns_to_update = rating_posn[unique]

            for posn in posns_to_update:
                if ratings[posn + 1] != ratings[posn]:
                    # left != mid and mid != right
                    if ratings[posn + 1] != ratings[posn + 2]:
                        candy_alloc[posn + 1] = max(candy_alloc[posn], candy_alloc[posn + 2]) + 1
                    # left != mid and mid == right
                    else:
                        candy_alloc[posn + 1] = candy_alloc[posn] + 1
                # left == mid and mid == right
                elif ratings[posn + 1] == ratings[posn + 2]:
                    candy_alloc[posn + 1] = 1
                # left == mid and mid != right
                else:
                    candy_alloc[posn + 1] = candy_alloc[posn + 2] + 1
        
        # 5. Sum up the candies allocated
        running_sum = 0
        for candy in candy_alloc:
            running_sum += candy

        return running_sum