# --- Параметры задачи (Обновленные) ---
L = 0.02        # Толщина стенки, м
lambda_ = 15.0  # Теплопроводность, Вт/(м*К)
c = 500.0       # Удельная теплоемкость, Дж/(кг*К)
rho = 7900.0    # Плотность, кг/м3
T0 = 300.0      # Начальная температура, °C

alpha1, Tg1 = 2000.0, 20.0  # Левая сторона
alpha2, Tg2 = 500.0, 80.0   # Правая сторона

# --- Параметры сетки ---
Nx = 20                 # Количество узлов по пространству
dx = L / (Nx - 1)       # Шаг по пространству
a = lambda_ / (c * rho) # Коэффициент температуропроводности

# Условие устойчивости: Fo = a * dt / dx^2 <= 0.5
Fo = 0.4
dt = Fo * (dx**2) / a   # Шаг по времени

total_time = 60         # Время моделирования, сек (уменьшено для наглядности)
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
with open("temperature_distribution_updated.txt", "w") as f:
    for time, temps in data:
        # Вывод первых, средних и последних 3 значений для краткости
        t_short = [round(t, 2) for t in (temps[:3] + temps[Nx//2-1:Nx//2+2] + temps[-3:])]
        line = f"Time: {time:6.2f} s | Temps (start/mid/end): {t_short}"
        print(line)
        f.write(line + "\n")
