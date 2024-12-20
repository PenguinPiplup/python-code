"""
Link to Problem: https://leetcode.com/problems/remove-nth-node-from-end-of-list/description/
This problem does not actually seem that relevant for a language like python
"""

# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:

        pointerfront = head
        pointerback = head
        for counter in range(n):
            pointerfront = pointerfront.next
        
        if pointerfront == None:
            return head.next
        else:
            pointerfront = pointerfront.next

        while pointerfront != None:
            pointerfront = pointerfront.next
            pointerback = pointerback.next

        pointerback.next = pointerback.next.next

        return head