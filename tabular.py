class Minterm: 
    def __init__(self, values, value):
        self._values = values
        self._value = value
        self._used = False

        self._values.sort()
    
    def __str__(self): # __str__ 메소드는 m*0, 4, 8, 12) = --00 형식으로 출력
        values = ", ".join([str(value) for value in self._values])
        return f"m({values}) = {self._value}"
    
    def __eq__(self, minterm):
        if type(minterm) != Minterm:
            return False

        return (
            self._value == minterm._value and
            self._values == minterm._values
        )
    def get_values(self): #minterm의 커버의 모든 implicant return
        return self._values
  
    def get_value(self): #이 최소값에 대한 비트 값('-010', '1010'등)을 반환
        return self._value
    
    def use(self):
        self._used = True
    
    def used(self): #minterm 사용 여부를 반환
        return self._used
        
    def plus(self, minterm): #가능한 경우 이 minterm과 지정한 minterm 결합

        #결합할 것과 동일한지 확인
        if self._value == minterm._value or self._values == minterm._values:
            return None
         
        #최소값의 차이의 양을 확인하고 또한 결과 문자열을 확인
        diff = 0
        result = ""

        #모든 비트 값을 반복
        for char in range(len(self._value)):

            #결합된 minterm과 이 minterm이 차이가 있는지 확인
            if self._value[char] != minterm._value[char]:
                diff += 1
                result += "-"
            
            #차이가 없을 경우
            else:
                result += self._value[char]
            
            #차이가 1보다 크면 최소값 결합 X
            if diff > 1:
                return None
        
        return Minterm(self._values + minterm._values, result)
        
class Tabular: #Tabular 확인
    def __init__(self, variables, values):
        self._variables = variables
        self._values = values

    def __get_bits(self, value): #지정된 값의 이진수 반환

        #일단 0으로 채우고 일치 여부 확인
        return bin(value)[2:].rjust(len(self._variables), "0")
    
    def __grouping(self):
        #값에서 비트 그룹핑
        
        #그룹핑한 2차원 배열 확인
        groups = []
        for count in range(len(self._variables) + 1):
            groups.append([])

        #값을 반복해서 확인
        for value in self._values:

            #1의 개수에 해당하는 비트 확인
            cnt = self.__get_bits(value).count("1")

            #맞는 그룹에 카운트 추가
            groups[cnt].append(Minterm([value], self.__get_bits(value)))
        
        return groups
        
    def __get_prime_implicants(self, groups = None): #prime implicants 정의

        if groups == None:
            groups = self.__grouping()
        
        #그룹이 하나라면 모든 minterm return
        if len(groups) == 1:
            return groups[0]
        
        #나머지 비교
        else:
            unused = []
            comparisons = range(len(groups) - 1)
            new_groups = [[] for c in comparisons]

            for compare in comparisons:
                group1 = groups[compare]
                group2 = groups[compare + 1]

                # 그룹1의 모든 요소를 그룹 2의 모든 요소와 비교
                for elem1 in group1:
                    for elem2 in group2:
                        
                        #결합하기
                        elem3 = elem1.combine(elem2)

                        # elem3이 None이 아닌 경우에 새 그룹에 추가
                        # elem3은 elem1과 elem2가 결합이 실패하면 None
                        if elem3 != None:
                            elem1.use()
                            elem2.use()
                            if elem3 not in new_groups[compare]:
                                new_groups[compare].append(elem3)
            
            # 미사용된 minterm
            for group in groups:
                for elem in group:
                    if not elem.used() and elem not in unused:
                        unused.append(elem)
            
            # Add recursive call
            for elem in self.__get_prime_implicants(new_groups):
                if not elem.used() and elem not in unused:
                    unused.append(elem)

            return unused

def __solution(self): #필요한 최소량의 prime implicant 확인
        
        #PI 확인
        prime_implicants = self.__get_prime_implicants(self.__grouping())
        
        #하나의 Implicant만 확인
        #EPI
        essential_prime_implicants = []
        values_used = [False] * len(self._values)

        for i in range(len(self._values)):
            value = self._values[i]

            uses = 0
            last = None
            for minterm in prime_implicants:
                if value in minterm.get_values():
                    uses += 1
                    last = minterm
            if uses == 1 and last not in essential_prime_implicants:
                for v in last.get_values():
                    values_used[self._values.index(v)] = True
                essential_prime_implicants.append(last)
        
        #모든 값이 사용되었는지 확인
        if values_used.count(False) == 0:
            return essential_prime_implicants
        
        #the fewest, largest circle 확인
        prime_implicants = [prime_implicant for prime_implicant in prime_implicants if prime_implicant not in essential_prime_implicants]

        #하나의 implicant만 남았는지 확인
        if len(prime_implicants) == 1:
            return essential_prime_implicants + prime_implicants

        # Create a power set from the remaining prime implicants and check which
        #   combination of prime implicants gets the simplest form
        return essential_prime_implicants + self.__power_set([
            self._values[index]
            for index in range(len(self._values))
            if not values_used[index]
        ], prime_implicants)
