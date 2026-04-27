import math

# --- Параметры задачи ---
L = 0.1         # Толщина стенки, м
lambda_ = 50.0  # Теплопроводность, Вт/(м*К)
c = 460.0       # Удельная теплоемкость, Дж/(кг*К)
rho = 7800.0    # Плотность, кг/м3
T0 = 20.0       # Начальная температура, °C

alpha1, Tg1 = 500.0, 100.0  # Левая сторона
alpha2, Tg2 = 100.0, 20.0   # Правая сторона

# --- Параметры сетки ---
Nx = 20                 # Количество узлов по пространству
dx = L / (Nx - 1)       # Шаг по пространству
a = lambda_ / (c * rho) # Коэффициент температуропроводности

# Условие устойчивости: Fo = a * dt / dx^2 <= 0.5
Fo = 0.45
dt = Fo * (dx**2) / a   # Шаг по времени

total_time = 300        # Время моделирования, сек
Nt = int(total_time / dt)

# Инициализация температурного поля
T = [T0 for _ in range(Nx)]

# --- Основной цикл решения ---
def solve():
    results = []
    
    # Сохраняем начальное состояние
    results.append((0.0, list(T)))
    
    current_T = T
    
    for step in range(1, Nt + 1):
        T_new = [0.0 for _ in range(Nx)]
        
        # 1. Граничное условие слева (балансовый метод)
        Bi1 = (alpha1 * dx) / lambda_
        T_new[0] = current_T[0] + 2 * Fo * (current_T[1] - current_T[0] + Bi1 * (Tg1 - current_T[0]))
        
        # 2. Внутренние узлы
        for i in range(1, Nx - 1):
            T_new[i] = current_T[i] + Fo * (current_T[i+1] - 2*current_T[i] + current_T[i-1])
            
        # 3. Граничное условие справа (балансовый метод)
        Bi2 = (alpha2 * dx) / lambda_
        T_new[Nx-1] = current_T[Nx-1] + 2 * Fo * (current_T[Nx-2] - current_T[Nx-1] + Bi2 * (Tg2 - current_T[Nx-1]))
        
        current_T = T_new
        
        # Сохранение состояния каждые 10% времени
        if step % (Nt // 10) == 0:
            results.append((step * dt, list(current_T)))
        
    return results

# Запуск и вывод
data = solve()
with open("temperature_distribution.txt", "w") as f:
    for time, temps in data:
        line = f"Time: {time:8.2f} s | Temps: {[round(t, 2) for t in temps]}"
        print(line)
        f.write(line + "\n")
