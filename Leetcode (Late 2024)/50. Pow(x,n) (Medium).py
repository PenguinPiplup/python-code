"""
Link to Problem: https://leetcode.com/problems/powx-n/description/
"""

class Solution:
    def myPow(self, x: float, n: int) -> float:
        if n == 0:
            return 1
        else:
            return self.PowHelper(x, n)

    def PowHelper(self, x, n):
        if n == 1:
            return x
        elif n == -1:
            return 1/x
        else:
            half_pow = self.PowHelper(x, n // 2)
            return half_pow * half_pow * self.myPow(x, n % 2)