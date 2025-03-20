def square(y):
	print("{} 的平方為 {}".format(y, y*y))


x = int(input("請輸入一個正整數："))

print("python程式測試", x)

if (x<0):
	print("您輸入的值是負數")
elif (x==0):
	print("您輸入的值是0")
else:
	for i in range(1,x+1):
		square(i)