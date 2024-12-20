"""
Problem Link: https://leetcode.com/problems/permutations/description/
"""

class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        # Base Case: if there is one integer left in nums, there is only one possible permutation
        if len(nums) == 1:
            return [nums]

        # acc stores all the possible permutations of the integers in array nums
        acc = []

        # we iterate through all the integers in nums (nums[0], nums[1], ... ) and find all the possible permutations 
        # where each specific integer (e.g. nums[i]) is placed in front
        for num in nums:
            nums_copy = nums.copy()

            # we remove one integer (i.e. nums[i]) from nums and we find the possible permutations of all the remaining integers using recursion. 
            # We then attach the integer (nums[i]) in front of every single possible permutation obtained via the recursive call.
            nums_copy.remove(num)
            prev_result = self.permute(nums_copy) # e.g. returns [[1,2], [2,1]]
            acc2 = []
            for lst in prev_result:
                lst = [num] + lst
                acc2 += [lst]
            acc += acc2
        return acc