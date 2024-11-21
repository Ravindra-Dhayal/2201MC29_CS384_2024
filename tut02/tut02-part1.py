num = int(input("enter the number :"))

while num>=10:
  total = 0
  temp = num
  while temp>0 :
    digit = temp%10
    total += digit
    temp = temp//10
    num = total
print("unitary sum :" , num)