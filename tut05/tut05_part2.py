def isValid(s: str) -> bool:
    st = []
    for ch in s:
        if ch in '([{':
            st.append(ch)
        elif ch == ')' and st and st[-1] == '(':
            st.pop()
        elif ch == ']' and st and st[-1] == '[':
            st.pop()
        elif ch == '}' and st and st[-1] == '{':
            st.pop()
        else:
            return False
    return not st

# Taking input from the user
s = input("Enter a string of brackets: ")
print(isValid(s))