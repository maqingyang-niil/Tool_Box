from scipy import signal
import matplotlib.pyplot as plt
import tempfile, os

class ControlController:
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