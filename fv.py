
n = int(input())
for _ in range(n):
    n,k,q = map(int,input().split())
    a = list(map(int,input().split()))
    for i in range(n):
        a[i] = int(a[i] < q+1)
    print(a,q)
    c = 0 
    tc = 0
    for i in a:
        if i == 1:
            c += 1
        else:
            if c == 0:
                tc += 0
                continue
            c = c-k+1
            p = c*(c+1)//2 
            tc += p 
            c = 0 
    if c > 0:
        c = c-k+1
        p = c*(c+1)//2 
        tc += p
    print(tc)
            