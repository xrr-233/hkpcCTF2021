from pwn import *

io = remote("chalp.hkcert21.pwnable.hk", 28157)

rv = io.recv(1024)
print(rv)
# 第一次
io.send('pkey\n')
rv = io.recv(1024)
print(rv)
# 第二次
moc = 1500000000000000000
io.send('send ' + str(hex(moc)) + '\n')
rv = io.recv(1024)
hex_m = int(str(rv, encoding='utf-8').split('\n')[0], 16)
k = 1
n = moc**17 - k * hex_m
while(moc**17 % n != hex_m):
    k+=1
print("n="+str(n))
#print(moc**17 % n)
#print(hex_m)
for i in range(15):
    io.send('a\n')
io.close()

#io.interactive()