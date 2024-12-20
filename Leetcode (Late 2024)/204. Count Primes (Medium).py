"""
Link: https://leetcode.com/problems/count-primes/description/
Description: Given an integer n, return the number of prime numbers that are strictly less than n.
Solution uses sieve of eratosthenes to filter out the primes
"""

class Solution:
    def countPrimes(self, n: int) -> int:
        if n < 2:
            return 0

        status = [True for _ in range(n)]
        status[0] = False # placeholder
        status[1] = False # 1 is not prime

        prime_count = 0
        for i in range(n):
            if status[i]:
                prime_count += 1
                for j in range(i*2, n, i):
                    status[j] = False
        
        return prime_count