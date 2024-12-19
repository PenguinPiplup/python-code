"""
Problem Link: https://leetcode.com/problems/find-score-of-an-array-after-marking-all-elements/description/
"""

class Solution:
    def findScore(self, nums: List[int]) -> int:
        nums_length = len(nums)
        marked = [False for _ in range(nums_length)]

        indices = {}
        unique_nums = []
        for index in range(nums_length):
            if nums[index] not in indices:
                indices[nums[index]] = [index]
                unique_nums += [nums[index]]
            else:
                indices[nums[index]] += [index]

        unique_nums.sort()
        score = 0

        for num in unique_nums:
            # mark all the possible elements and add to score
            for position in indices[num]:
                if not marked[position]:
                    marked[position] = True
                    if position > 0:
                        marked[position - 1] = True
                    if position < nums_length - 1:
                        marked[position + 1] = True
                    score += num

        return score