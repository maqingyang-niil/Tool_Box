from scipy import signal
import matplotlib.pyplot as plt
import matplotlib
import tempfile, os
import numpy as np
import io

from scipy.stats import alpha

matplotlib.use('Agg')

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
        ax.set_xlabel('real axis')
        ax.set_ylabel('imaginary axis')
        ax.set_title('root distribution')
        ax.grid(True, linestyle=':', alpha=0.6)
        ax.set_aspect('equal')
        plt.tight_layout()


        path = os.path.join(tempfile.gettempdir(), "_poles_plot.png")
        fig.savefig(path, dpi=150)
        plt.close(fig)
        return path
    #计算根轨迹
    def root_locus(self,num:list,den:list)->str:
        K_values=np.linspace(0,300,3000)

        num_padded=np.zeros_like(den,dtype=float)
        num_padded[-len(num):]=num
        all_roots=[]
        for k in K_values:
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
