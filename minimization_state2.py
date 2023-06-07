import pandas as pd
import numpy as np

input_file = r'D:\Thiết kế luận lý số\Bài tập lớn\Do_an\Testcase\TestCase\autoTest21.xlsx'
state_table = pd.read_excel (input_file)

present_states = state_table.iloc [1:,0].values
next_states0 = state_table.iloc [1:,1:2].values
next_states0.tolist() 
next_states1 = state_table.iloc [1:,2:3].values
next_states1.tolist()
output0 = state_table.iloc [1:,3:4].values
output1 = state_table.iloc [1:,4:5].values

# Cac ham gom nhom:
def create_vector_list (A,B,C):
    A = []
    for i in range (len (B)):
        A.append ([])
        A[i].append (B[i][0])
        A[i].append (C[i][0])
    return A

def create_group_list (A,B,C):
    A = []
    for i in range(4):
        if i == 0 or i == 1: binary_array = [int(bit) for bit in format(i, '02b')]
        else: binary_array = [int(bit) for bit in bin(i)[2:]]
        A.append ([])
        for j in range (len(B)):
            if binary_array == B[j] :
                A[i].append (C[j])
            else: continue
    
    A = list(filter(lambda x: len(x) > 0, A))
    return A

def update_group_list_NS (A,B,C):
    A = []
    for i in range (len(B)):
        A.append([])
        for element in B[i]:
            A[i].append (C[int(element[1:])])
    return A
    
######################################################
# xu ly - gom nhom :
next_states = []
Group_PS = []
Group_NS = []
Group_OP = []

next_states = create_vector_list (next_states, next_states0, next_states1)
Group_OP = create_vector_list (Group_OP,output0, output1)
Group_PS = create_group_list (Group_PS,Group_OP,present_states)
Group_NS = create_group_list (Group_NS,Group_OP,next_states)


########################################################
# Xu ly vong lap:
#1 Hàm thay thế. (Hàm chỉ dùng riêng cho nhóm NS và chỉ dùng được cho mảng 1 chiều)
#2 Hàm kiểm tra
#3 Phân hoạch lại.

def replace_child_element (A,B):
    #if isinstance(A, np.ndarray) :A = A.tolist()
    for i in range (len(A)):
        for j in range (len(B)):
            if A[i] in B[j]: 
                A[i] = f'G{j}'
    return A

def Replace (A,B,C,D,E):
    B = replace_child_element(B,E)  # B <=> next_states0
    C = replace_child_element(C,E)  # C <=> next_states1
    D = create_vector_list (D,B,C)  # D <=> next_states
    A = update_group_list_NS (A,E,D)   # A <=> Group_NS
    #E <=> Group_PS
    
    return A

def check_diff(A):
    for i in range(len(A)):
        if not all(element == A[i][0] for element in A[i]):
            return False
    return True

def update_group_list_PS (A,B):
    A_copy = A.copy()
    diff = []
    A = []
    for i in range (len(B)):
        diff.append ([])
        if all(element == B[i][0] for element in B[i]): A.append (A_copy[i])
        else:
            temp = B[i][0]
            temp_copy = A_copy[i].copy()
            for j in range (len(B[i])):
                if B[i][j] != temp :
                    diff[i].append(A_copy[i][j])
                    temp_copy.remove(A_copy[i][j])
            A.append(temp_copy)
    
    diff = list(filter(lambda x: len(x) > 0, diff))
    for i in range (len(diff)):
        A.append (diff [i])
    return A 

ns0_copy = next_states0.copy()
ns1_copy = next_states1.copy()
Group_NS = Replace (Group_NS, ns0_copy, ns1_copy, next_states, Group_PS)

while not check_diff (Group_NS):
    Group_PS = update_group_list_PS (Group_PS, Group_NS)

    ns0_copy = next_states0.copy()
    ns1_copy = next_states1.copy()
    Group_NS = Replace (Group_NS, ns0_copy, ns1_copy, next_states, Group_PS)
  
#########################################################
def find_minimum_suffix(arr):
    min_suffix_element = min(arr, key=lambda x: int(x[1:]))
    return min_suffix_element

def sort_by_suffix(arr):
    sorted_arr = sorted(arr, key=lambda x: int(x[1:]))
    return sorted_arr

def update_minimize_ns (A, B):
    for i in range (len(A)):
        for j in range (len(B)):
            if A[i] in B[j]: 
                A[i] = min(B[j], key=lambda x: int(x[1:]))
    return A

def get_suffix(element):
    suffix = element[1:]
    return suffix

Minimize_PS = []
Minimize_NS0 = []
Minimize_NS1 = []
Minimize_OP0 = []
Minimize_OP1 = []

for i in range (len(Group_PS)):
    Minimize_PS.append(find_minimum_suffix (Group_PS[i]))
Minimize_PS = sort_by_suffix (Minimize_PS)

next_states0 = update_minimize_ns(next_states0, Group_PS)
next_states1 = update_minimize_ns(next_states1, Group_PS)

for i in range (len(Minimize_PS)):
    s = int(get_suffix(Minimize_PS[i]))
    Minimize_NS0.append (next_states0[s])
    Minimize_NS1.append (next_states1[s])
    Minimize_OP0.append (output0[s])
    Minimize_OP1.append (output1[s])

TTKT0 = np.vstack(Minimize_NS0)
TTKT1 = np.vstack(Minimize_NS1)
Output0 = np.vstack(Minimize_OP0)
Output1 = np.vstack(Minimize_OP1)

data = {
    'TTHT': Minimize_PS,
    'TTKT0': TTKT0[:,0],
    'TTKT1': TTKT1[:,0],
    'Output0': Output0[:,0],
    'Output1': Output1[:,0]
}

df = pd.DataFrame(data)
output_file = r'D:\Thiết kế luận lý số\Bài tập lớn\Do_an\Result\Result_autotest\Result21.xlsx'
df.to_excel(output_file, index=False)

print (Group_PS)
print (Group_NS)
print ('so trang thai sau rut gon: ', len (Minimize_PS))