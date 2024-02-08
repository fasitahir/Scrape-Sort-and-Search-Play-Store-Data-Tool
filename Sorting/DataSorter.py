import pandas as pd
import re
import time
'.................................Selection Sort.............................................'

def Selectionsort(arr, start, end, column, type):
    if type == "ascending":
        for i in range(start, end-1):
            minIndex=i
            for j in range(i+1,end):
                if arr[j][column] < arr[minIndex][column]:
                    minIndex=j
            arr[i],arr[minIndex]=arr[minIndex],arr[i]
        return arr
    
    elif type == "descending":
        for i in range(start, end-1):
            minIndex=i
            for j in range(i+1,end):
                if arr[j][column] > arr[minIndex][column]:
                    minIndex=j
            arr[i],arr[minIndex]=arr[minIndex],arr[i]
        return arr


'.................................Bubble sort.............................................'
def Bubblesort(arr, start, end, column, type):
    if type == "ascending":
        swap = True
        for i in range(start, end):        
            for j in range(start, end - i - 1):
                if arr[j][column] > arr[j + 1][column]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    swap = False
            if swap:
                break
        return arr
    
    elif type == "descending":
        swap = True
        for i in range(start, end):        
            for j in range(start, end - i - 1):
                if arr[j][column] < arr[j + 1][column]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    swap = False
            if swap:
                break
        return arr
    
'.................................Insertion sort.............................................'

def InsertionSort(arr, start, end,column, type):
    if type == "ascending":
        flag = True
        for i in range(start + 1, end):
            key = arr[i]
            j = i - 1
            while arr[j][column] > key[column] and j >= start:
                arr[j + 1] = arr[j]
                j = j - 1
                arr[j + 1] = key

                flag = False
        if flag == True:
            return arr

        return arr
    
    elif type == "descending":
        flag = True
        for i in range(start + 1, end):
            key = arr[i]
            j = i - 1
            while arr[j][column] < key[column] and j >= start:
                arr[j + 1] = arr[j]
                j = j - 1
                arr[j + 1] = key

                flag = False
        if flag == True:
            return arr

        return arr
    
'.................................Merge sort.............................................'

def Merge(array, start, end, mid, column, type):
    if type == "ascending":
        left = array[start:mid + 1]
        right = array[mid + 1:end + 1]

        i = j = 0
        k = start

        while i < len(left) and j < len(right):
            if left[i][column] <= right[j][column]:
                array[k] = left[i]
                i += 1
            else:
                array[k] = right[j]
                j += 1
            k += 1

        while i < len(left):
            array[k] = left[i]
            i += 1
            k += 1

        while j < len(right):
            array[k] = right[j]
            j += 1
            k += 1

    elif type == "descending":
        left = array[start:mid + 1]
        right = array[mid + 1:end + 1]

        i = j = 0
        k = start

        while i < len(left) and j < len(right):
            if left[i][column] >= right[j][column]:
                array[k] = left[i]
                i += 1
            else:
                array[k] = right[j]
                j += 1
            k += 1

        while i < len(left):
            array[k] = left[i]
            i += 1
            k += 1

        while j < len(right):
            array[k] = right[j]
            j += 1
            k += 1

def MergeSort(array, start, end,column, type):
    if start < end:
        mid = start + (end - start) // 2
        MergeSort(array, start, mid,column, type)
        MergeSort(array, mid + 1, end,column, type)
        Merge(array, start, end, mid,column, type)
    
'.................................Quick sort.............................................'

def partition(A, p, r,column, type):
    if type == "ascending":
        x = A[r]  #pivot
        i = p - 1 #minimum index

        for j in range(p, r):
            if A[j][column] <= x[column]:
                i = i + 1
                A[i], A[j] = A[j], A[i]

        A[i + 1], A[r] = A[r], A[i + 1]
        return i + 1 #return new pivot
    
    elif type == "descending":
        x = A[r]  #pivot
        i = p - 1 #minimum index

        for j in range(p, r):
            if A[j][column] >= x[column]:
                i = i + 1
                A[i], A[j] = A[j], A[i]

        A[i + 1], A[r] = A[r], A[i + 1]
        return i + 1 #return new pivot

def QuickSort(A, p, r, column, type):
    if p < r:
        q = partition(A, p, r,column, type)
        QuickSort(A, p, q - 1,column, type) #less than pivot
        QuickSort(A, q + 1, r,column, type) #greater than pivot

'.................................Heap sort.............................................'

def Heapify(arr, n, i,column, type):
    
    if type == "ascending":
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2

        if left < n and arr[left][column] > arr[largest][column]:
            largest = left
        
        if right < n and arr[right][column] > arr[largest][column]:
            largest = right
        
        if largest != i:
            arr[largest],arr[i] = arr[i], arr[largest]
            Heapify(arr, n, largest, column, type)
    
    elif type == "descending":
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2

        if left < n and arr[left][column] < arr[largest][column]:
            largest = left
        
        if right < n and arr[right][column] < arr[largest][column]:
            largest = right
        
        if largest != i:
            arr[largest],arr[i] = arr[i], arr[largest]
            Heapify(arr, n, largest, column, type)
    
def HeapSort(arr,column, type):
    n = len(arr)

    for i in range(n // 2 - 1, -1, -1):
        Heapify(arr, n, i,column, type)

    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        Heapify(arr, i, 0,column, type)

'.................................Shell sort.............................................'

def ShellSort(arr, column, type):
    
    if type == "ascending":        
        n = len(arr)
        gap = n // 2
        while gap > 0:
            for i in range(gap, n):
                temp = arr[i]
                j = i
                while j >= gap and arr[j - gap][column] > temp[column]:
                    arr[j] = arr[j - gap]
                    j -= gap
                arr[j] = temp
            gap //= 2

        return arr
    
    elif type == "descending":        
        n = len(arr)
        gap = n // 2
        while gap > 0:
            for i in range(gap, n):
                temp = arr[i]
                j = i
                while j >= gap and arr[j - gap][column] < temp[column]:
                    arr[j] = arr[j - gap]
                    j -= gap
                arr[j] = temp
            gap //= 2

        return arr
    
'.................................Radix Sort.............................................'

def InsertionSortForRadix(array,exp,column, type):
    
    if type == "ascending":        
        for i in range(1,len(array)):
            j=i-1
            key=array[i]
            while j>=0 and key[column]//exp < array[j][column]//exp:
                array[j+1]=array[j]
                j-=1
            array[j+1]=key

    elif type == "descending":        
        for i in range(1,len(array)):
            j=i-1
            key=array[i]
            while j>=0 and key[column]//exp < array[j][column]//exp:
                array[j+1]=array[j]
                j-=1
            array[j+1]=key

def RadixSort(array,column, type):
    max_element=max(array,key=lambda x: x[column])[column]
    exp=1
    while max_element//exp>0:
        InsertionSortForRadix(array,exp,column, type)
        exp=exp*10
    return array

'.................................PigeonHole Sort.............................................'

def PigeonHoleSort(arr, column, Type):

    key = [item[column] for item in arr]
    minIndex = min(key)
    maxIndex = max(key)
    rangeValues = maxIndex - minIndex + 1
    pigeonholes = [0] * rangeValues
    sortedArray = []

    for item in arr:
        keys = item[column] - minIndex
        pigeonholes[keys] += 1

    if Type == 'ascending':
        for i in range(rangeValues):
            while pigeonholes[i] > 0:
                value = i + minIndex
                for item in arr:
                    if item[column] == value:
                        sortedArray.append(item)
                        pigeonholes[i] -= 1
    elif Type == 'descending':
        for i in range(rangeValues - 1, -1, -1):
            while pigeonholes[i] > 0:
                value = i + minIndex
                for item in arr:
                    if item[column] == value:
                        sortedArray.append(item)
                        pigeonholes[i] -= 1

    return sortedArray

'.................................Counting Sort.............................................'

def CountingSort(array, column, type):
    # Extract the column values to sort
    values = [item[column] for item in array]
    m = max(values)
    n = min(values)

    Count = [0] * (m - n + 1)
    output = [0] * len(array)

    for val in values:
        k = val - n
        Count[k] += 1

    for i in range(1, len(Count)):
        Count[i] += Count[i - 1]
    
    if type == "ascending":
        for i in range(len(array) - 1, -1, -1):
            j = values[i] - n
            Count[j] -= 1
            output[Count[j]] = array[i]

    if type == "descending":
        for i in range(0 ,len(array)):
            j = values[i] - n
            Count[j] -= 1
            output[Count[j]] = array[i]
    

    return output

'.................................Cocktail Shaker Sort.............................................'

def CockTailShaker(arr, column, type):
    n = len(arr)
    flag = True
    if type == "ascending":

        for i in range(0, n):
            for j in range(0, n-i-1):
                if arr[j][column] > arr[j+1][column]:
                    arr[j], arr[j+1] = arr[j+1], arr[j]
                    flag = True
            if flag == False:
                break

            for j in range(n-2-i, -1+i, -1):
                if arr[j][CockTailShaker] > arr[j+1][CockTailShaker]:
                    arr[j], arr[j+1] = arr[j+1], arr[j]
                    flag = True
            
            if flag == False:
                break
    if type == "descending":
        for i in range(0, n):
            for j in range(0, n-i-1):
                if arr[j][column] > arr[j+1][column]:
                    arr[j], arr[j+1] = arr[j+1], arr[j]
                    flag = True
            if flag == False:
                break

            for j in range(n-2-i, -1+i, -1):
                if arr[j][CockTailShaker] > arr[j+1][CockTailShaker]:
                    arr[j], arr[j+1] = arr[j+1], arr[j]
                    flag = True
            
            if flag == False:
                break
    return arr

'.................................Hybrid Merge Sort.............................................'

def HybridMergeSort(array, start, end, column , Type):
    minRun = 70
    n = len(array)

    for i in range(0, n, minRun):
        end = min((i + n - 1), (n - 1))
        InsertionSortHybridMerge(array, i, end,column, Type)

    m = minRun
    while m < n:
        for j in range(0, n, m * 2):
            mid = min((n - 1), (j + m - 1))
            if m < mid:
                Merge(array, start, mid, end, column,Type)
        m = m * 2
    return array


def InsertionSortHybridMerge(arr, start, end, column , Type):
    if Type == 'ascending':
        for i in range(start + 1, end + 1):
            j = i
            
            while j > start and arr[j][column] < arr[j - 1][column]:
                arr[j], arr[j - 1] = arr[j - 1], arr[j]
                j -= 1
    
    elif Type == 'descending':
        for i in range(start + 1, end + 1):
            j = i
            while j > start and arr[j][column] > arr[j - 1][column]:
                arr[j], arr[j - 1] = arr[j - 1], arr[j]
                j -= 1
            
'.................................Extracting Integers from string.............................................'

def extract_integers(text):
    if isinstance(text, str):
        text = text.upper()  # Convert to uppercase for case insensitivity
        numeric_part = re.search(r'(\d+\.\d+|\d+)', text)
        if numeric_part:
            numeric_value = float(numeric_part.group())
            if 'K' in text:
                return int(numeric_value * 1000)
            elif 'M' in text:
                return int(numeric_value * 1000000)
            elif 'B' in text:
                return int(numeric_value * 1000000000)
            else:
                return int(numeric_value)
        return int(text)  # Handle cases without 'K', 'M', or 'B' suffix
    return None

def extract_integers_Price(text):
    if isinstance(text, str):
        text = text.upper()  # Convert to uppercase for case insensitivity
        numeric_part = float(re.search(r'(\d+\.\d+|\d+)', text).group()) if re.search(r'(\d+\.\d+|\d+)', text) else None
        return numeric_part
    return None


def extract_integers_to_string(text):
    if isinstance(text, str):
        text = text.upper()  # Convert to uppercase for case insensitivity
        if 'K' in text:
            numeric_part = int(re.search(r'(\d+\.\d+|\d+)', text).group())
            return f'{int(numeric_part * 1000)}K'
        elif 'M' in text:
            numeric_part = int(re.search(r'(\d+\.\d+|\d+)', text).group())
            return f'{int(numeric_part * 1000000)}M'
        elif 'B' in text:
            numeric_part = int(re.search(r'(\d+\.\d+|\d+)', text).group())
            return f'{int(numeric_part * 1000000000)}B'
        else:
            numbers = re.findall(r'\d+', text)
            if numbers:
                return numbers[0]
    return None


def dataSorter(algorithm, column, type):
    print("Started")
    columnName = column
    file = "D:\\FasiTahir\\DSA\\Mid Project\\ScrapedData.csv"
    df = pd.read_csv(file, dtype={columnName: str})
    df = df.dropna(subset=[columnName])
    if column == "Rating" or column == "Price":
        df[columnName] = df[columnName].apply(extract_integers_Price)
    
    elif column == "Reviews" or column == "Downloads":
        df[columnName] = df[columnName].apply(extract_integers)
    
    records = df.to_dict('records')
    
    start_time = time.time()
    
    if algorithm == "MergeSort":
        MergeSort(records, 0, len(records) - 1, columnName, type)
    
    elif algorithm == "RadixSort":
        RadixSort(records, column, type)

    elif algorithm == "PigeonHoleSort":
        records = PigeonHoleSort(records, columnName, type)
    
    elif algorithm == "CountingSort":
        records = CountingSort(records, columnName, type)

    elif algorithm == "HeapSort":
        HeapSort(records, column, type)
    
    elif algorithm == "QuickSort":
        QuickSort(records, 0, len(records)-1, column, type)
    
    elif algorithm == "ShellSort":
        ShellSort(records, column, type)
    
    elif algorithm == "SelectionSort":
        Selectionsort(records, 0, len(records), column, type)
    
    elif algorithm == "InsertionSort":
        InsertionSort(records, 0, len(records), column, type)
    
    elif algorithm == "BubbleSort":
        Bubblesort(records, 0, len(records), column, type)

    elif algorithm == "CocktailShaker":
        CockTailShaker(records, column, type)

    elif algorithm == "HybridMergeSort":
        HybridMergeSort(records, 0, len(records)-1, column, type)
    
    end_time = time.time()

    sorted_df = pd.DataFrame(records)
    sorted_df.to_csv("D:\\FasiTahir\\DSA\\Mid Project\\ScrapedData.csv", index=False)
    print("Loaded in CSV")

    elapsed_time = end_time - start_time
    
    return elapsed_time

def MultiColumnMerge(arr, start, end, mid, column):
    left = arr[start:mid + 1]
    right = arr[mid + 1:end + 1]
    
    i = j = 0
    k = start
    
    while i < len(left) and j < len(right):
        if MultiLevelCompare(left[i], right[j], column):
            arr[k] = left[i]
            i += 1
        else:
            arr[k] = right[j]
            j += 1
        k += 1
    
    while i < len(left):
        arr[k] = left[i]
        i += 1
        k += 1
    
    while j < len(right):
        arr[k] = right[j]
        j += 1
        k += 1

def MultiColumnMergeSort(arr, start, end, column):
    if start < end:
        mid = start + (end - start) // 2
        MultiColumnMergeSort(arr, start, mid, column)
        MultiColumnMergeSort(arr, mid + 1, end, column)
        MultiColumnMerge(arr, start, end, mid, column)

def MultiLevelCompare(leftArray, rightArray, columns):
    for col in columns:
        left_val = leftArray[col]
        right_val = rightArray[col]
        
        if isinstance(left_val, (int, float)) and isinstance(right_val, (int, float)):
            if left_val < right_val:
                return True
            elif left_val > right_val:
                return False
        elif isinstance(left_val, str) and isinstance(right_val, str):
            if left_val < right_val:
                return True
            elif left_val > right_val:
                return False

    return False

def MultiColumnSort(columnNames):
    file = "D:\\FasiTahir\\DSA\\Mid Project\\ScrapedData.csv"
    
    for column in columnNames:
        df = pd.read_csv(file, dtype={column: str})
        df = df.dropna(subset=[column])

        if column == "Rating" or column == "Price":
            df[column] = df[column].apply(extract_integers_Price)
        elif column == "Reviews" or column == "Downloads":
            df[column] = df[column].apply(extract_integers)
        else:
            df[column] = df[column].astype(str)


    records = df.to_dict('records')
    MultiColumnMergeSort(records, 0, len(records) - 1, columnNames)
    sorted_df = pd.DataFrame(records)
    sorted_df.to_csv("D:\\FasiTahir\\DSA\\Mid Project\\ScrapedData.csv", index=False)
    print("Loaded in CSV")

#columnNames = [ "Name", "Price", "Category", "Downloads", "Rating", "Updated Date", "Reviews"]

#MultiColumnSort(columnNames)

#dataSorter("MergeSort", "Name", "ascending")
#dataSorter("CountingSort", "Reviews", "descending")