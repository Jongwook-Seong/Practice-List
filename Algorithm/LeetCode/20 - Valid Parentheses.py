class Solution:
    def isValid(self, s: str) -> bool:
        l = len(s)
        stack = []
        o = ['(', '{', '[']
        c = [')', '}', ']']
        if l == 0: return True
        elif l % 2 != 0: return False
        elif s[0] in c: return False
        elif s[l-1] in o: return False
        for p in s:
            if p in o: stack.append(p)
            elif p in c:
                ptype = c.index(p)
                if len(stack) > 0 and stack.pop() == o[ptype]: continue
                else: return False
        if len(stack) == 0: return True