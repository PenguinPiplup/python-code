"""
Link to Problem: https://leetcode.com/problems/jump-game-ii/description/
This solution uses breadth-first search
"""

class Solution:
    def jump(self, nums: List[int]) -> int:
        n = len(nums)
        if n == 1:
            return 0

        current_pos = 0
        frontier = []
        explored = [False for _ in range(n)]

        # e.g. [2,1,1]
        if current_pos + nums[current_pos] >= n - 1:
            return 1

        # e.g. [2,1,2,1]
        for jump in range (nums[current_pos], 0, -1):
            frontier += [[current_pos, current_pos + jump]]

        while True:
            first = frontier[0]
            frontier.pop(0)

            if nums[first[-1]] == 0:
                pass
            elif first[-1] + nums[first[-1]] >= n - 1:
                return len(first)
            else:
                # add new things to frontier
                for jump2 in range (nums[first[-1]], 0, -1):
                    new_pos = first[-1] + jump2
                    if new_pos >= n:
                        pass
                    elif not explored[new_pos]:
                        first2 = first.copy()
                        first2 += [new_pos]
                        frontier += [first2]
                        explored[new_pos] = True