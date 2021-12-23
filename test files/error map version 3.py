length = 40
overlap = 0.25
number_of_chunks = 5

# chunk_1 => 0 ~ 12.5
# chunk_2 +> 7.5 ~ 20

chunk_length = int(length / (number_of_chunks - (number_of_chunks - 1 )* overlap))
print(chunk_length)
step = int(chunk_length * (1 - (overlap)) + 0.5)
print(step)
for i in range(1, number_of_chunks+1):
    pass

list = [[1,2,3,4,5], [10,2,45,56],[12,213,345]]

print(list[0])

def hello():
    return 20, 2

a, b = hello()
print(a)