s=input("Enter the string : ")
n=len(s)
i=0
ans=''
while(i<n):
  j=i
  c=0
  while(j<n and s[j]==s[i]):
    c+=1
    j+=1
  ans+=s[i]
  ans+=str(c)
  i=j

print("Enter the output : ",ans)