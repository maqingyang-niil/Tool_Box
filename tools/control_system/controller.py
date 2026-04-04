from scipy import signal
import matplotlib.pyplot as plt
import matplotlib
import tempfile, os
import numpy as np
matplotlib.rcParams['font.family'] = ['Microsoft YaHei']  # 微软雅黑
matplotlib.rcParams['axes.unicode_minus'] = False          # 负号正常显示

matplotlib.use('Agg')

def steady_or_not(den:list)->bool:
    # 判断系统是否稳定
    n = len(den)
    rows = (n + 1) // 2
    table = np.zeros((n, rows))
    table[0, :len(den[0::2])] = den[0::2]
    table[1, :len(den[1::2])] = den[1::2]

    for i in range(2, n):
        for j in range(rows - 1):
            pivot = table[i - 1, 0]
            if pivot == 0:
                pivot = 1e-10
                table[i - 1, 0] = pivot
            table[i, j] = (pivot * table[i - 2, j + 1] - table[i - 2, 0] * table[i - 1, j + 1]) / pivot

    first_col = table[:, 0]
    sign_changes = sum(
        1 for i in range(1, len(first_col))
        if first_col[i] * first_col[i - 1] < 0
    )
    return sign_changes==0

class ControlController:
    #计算闭环根
    def get_polar(self,num:list,den:list)->str:
        tf=signal.TransferFunction(num,den)
        poles=tf.poles

        fig, ax = plt.subplots()
        ax.axhline(0,color='black',linewidth=0.8,linestyle='--')
        ax.axvline(0,color='black',linewidth=0.8,linestyle='--')

        for i,p in enumerate(poles):
            ax.plot(p.real, p.imag, 'rx', markersize=12, markeredgewidth=2)
            ax.annotate(
                f'  p{i + 1} = {p.real:.3f}{f"{p.imag:+.3f}j" if p.imag != 0 else ""}',
                xy=(p.real, p.imag),
                fontsize=9,
                color='red'
            )
        ax.set_xlabel('实轴')
        ax.set_ylabel('虚轴')
        ax.set_title('特征根分布')
        ax.grid(True, linestyle=':', alpha=0.6)
        ax.set_aspect('equal')
        plt.tight_layout()


        path = os.path.join(tempfile.gettempdir(), "_poles_plot.png")
        fig.savefig(path, dpi=150)
        plt.close(fig)
        return path
    #计算根轨迹
    def root_locus(self,num:list,den:list)->str:
        k_values=np.linspace(0,300,3000)

        num_padded=np.zeros_like(den,dtype=float)
        num_padded[-len(num):]=num
        all_roots=[]
        for k in k_values:
            cl_den=den+k*num_padded
            all_roots.append(np.roots(cl_den))
        all_roots=np.array(all_roots)

        plt.figure(figsize=(8,6))
        plt.plot(all_roots.real,all_roots.imag,color='b',alpha=0.5)
        open_loop_poles = np.roots(den)
        open_loop_zeros = np.roots(num)
        plt.scatter(open_loop_poles.real, open_loop_poles.imag, marker='x', color='red', label='Poles')
        plt.scatter(open_loop_zeros.real, open_loop_zeros.imag, marker='o', edgecolors='blue', facecolors='none',
                    label='Zeros')

        plt.axhline(0, color='black', lw=1)  # 实轴
        plt.axvline(0, color='black', lw=1)  # 虚轴
        plt.grid(True)

        path = os.path.join(tempfile.gettempdir(), "_root_locus.png")
        plt.savefig(path, dpi=100)
        plt.close()
        return path

    def bode_graph(self,num:list,den:list)->str:
        tf=signal.TransferFunction(num,den)
        w=np.logspace(-2,5,10000)
        w,mag,phase=signal.bode(tf,w=w)
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))

        ax1.semilogx(w, mag)
        ax1.set_ylabel('幅值 (dB)')
        ax1.set_title('伯德图')
        ax1.grid(True, which='both')

        ax2.semilogx(w, phase)
        ax2.set_ylabel('相位 (°)')
        ax2.set_xlabel('频率 (rad/s)')
        ax2.grid(True, which='both')

        plt.tight_layout()

        path = os.path.join(tempfile.gettempdir(), "_bode_plot.png")
        fig.savefig(path, dpi=150)
        plt.close(fig)
        return path

    def nyquist_graph(self,num:list,den:list)->str:
        tf=signal.TransferFunction(num,den)
        w=np.logspace(-3,6,100000)
        w,H=signal.freqresp(tf,w)

        plt.figure(figsize=(8, 8))
        plt.plot(H.real, H.imag, 'b', label='ω: 0 → +∞')
        plt.plot(H.real, -H.imag, 'b--', label='ω: 0 → -∞')
        plt.plot(-1, 0, 'r+', markersize=12, markeredgewidth=2, label='(-1, 0)')

        plt.xlabel('实轴')
        plt.ylabel('虚轴')
        plt.title('奈奎斯特图')
        plt.axhline(0, color='k', linewidth=0.5)
        plt.axvline(0, color='k', linewidth=0.5)
        plt.grid(True)

        path=os.path.join(tempfile.gettempdir(),"_nyquist_plot.png")
        plt.savefig(path,dpi=100)
        plt.close()
        return path

    def step_response(self,
                      num:list,
                      den:list,
                      t_final:int,
                      err_bound:float
                      )->tuple[str,float,float,float,float,bool]:
        steady = steady_or_not(den)
        tf = signal.TransferFunction(num, den)
        t = np.linspace(0, t_final, 800 * t_final)
        t, y = signal.step(tf, T=t)

        plt.plot(t, y)
        plt.xlabel('时间 (s)')
        plt.ylabel('输出')
        plt.title('单位阶跃响应')
        plt.grid(True)

        path = os.path.join(tempfile.gettempdir(), "_step_response_plot.png")
        plt.savefig(path, dpi=100)
        plt.close()

        if not steady:
            return path,0,0,0,0,steady
        else:
            threshold = err_bound
            if threshold <= 0 or threshold >= 1:
                raise ValueError(f"误差范围必须在0到1之间，当前输入：{err_bound}")

            steady_state = num[-1] / den[-1]
            peak = np.max(y)
            if peak > steady_state:  # 欠阻尼系统
                overshoot = (peak - steady_state) / steady_state * 100
                peak_time = t[np.argmax(y)]

                t_100 = t[np.where(y >= steady_state)[0][0]]
                rise_time = t_100
            else:  # 过阻尼系统
                overshoot = 0
                peak_time = 0
                t_10 = t[np.where(y >= 0.1 * steady_state)[0][0]]
                t_90 = t[np.where(y >= 0.9 * steady_state)[0][0]]
                rise_time = t_90 - t_10

            outside = np.where(np.abs(y - steady_state) > threshold * np.abs(steady_state))[0]
            if len(outside) == 0:
                settling_time = 0.0
            else:
                settling_time = float(t[outside[-1]])
            return path, settling_time, overshoot, peak_time, rise_time, steady






















