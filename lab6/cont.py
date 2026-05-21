import numpy as np
import cv2
from scipy.signal import convolve2d
import scipy.fft as scipy
import matplotlib.pyplot as plt

FIG_SIZE = (12, 12)
DPI = 300 

folder = "C:\\Users\\Professional\\Here i live\\Uni\\FM\\lab6\\Paper\\images\\"

img = cv2.imread(folder+"noita.png")
print(img)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imwrite(folder+"noita_gray.png", gray)


def gauss_ker(N):
    A = np.zeros((N, N))
    sigma = (N-1)/6
    for i in range(N):
        for j in range(N):
            A[i][j] = np.exp(-((i - (N+1)/2)**2 + (j - (N+1)/2)**2)/(2*sigma**2))

    s = sum(sum(A))
    return A/s

def block_ker(N):
    A = np.zeros((N, N))
    A += 1
    s = sum(sum(A))
    
    return A/s

def ker_appl(ker, img, type):
    N, M = img.shape
    kh, kw = ker.shape

    Me = M + kw - 1
    Ne = N + kh - 1

    img_e = np.zeros((Ne, Me))
    img_e[:N, :M] = img
    
    ker_e = np.zeros((Ne, Me))
    ker_e[:kh, :kw] = ker

    fur_img = scipy.fft2(img_e)
    fur_ker = scipy.fft2(ker_e)

    img_filt = fur_img*fur_ker
    

    plt.figure(figsize=FIG_SIZE, dpi=DPI)
    plt.imshow(np.log(abs(img_filt)), cmap='gray')
    plt.axis('off')
    plt.savefig(
        folder+f"fur_log_filtered{type}.png",
        bbox_inches='tight',
        pad_inches=0,
        dpi=DPI
    )
    plt.close()

    result_pad = np.real(scipy.ifft2(img_filt))
    result_pad = np.clip(result_pad, 0, 255).astype(np.uint8)
    start_h = kh // 2
    start_w = kw // 2
    filtered_img = result_pad[start_h:start_h+M, start_w:start_w+N]

    plt.figure(figsize=FIG_SIZE, dpi=DPI)
    plt.imshow(filtered_img, cmap='gray')
    plt.axis('off')
    plt.savefig(
        folder+f"filtered_img_{type}.png",
        bbox_inches='tight',
        pad_inches=0,
        dpi=DPI
    )
    plt.close()

g_k = []
b_k = []

N = [10, 40, 120]

for n in N:
    g_k.append(gauss_ker(n))
    b_k.append(block_ker(n))

K_s = np.array([
    [0, -1, 0],
    [-1, 5, -1],
    [0, -1, 0]
])

K_e = np.array([
    [-1, -1, -1],
    [-1, 8, -1],
    [-1, -1, -1]
])

fur_img = scipy.fftshift(scipy.fft2(gray))

magnitude = np.log1p(abs(fur_img))
plt.figure(figsize=FIG_SIZE, dpi=DPI)
plt.imshow(magnitude, cmap="gray")
plt.title('Амплитудный спектр (центр = 0 Гц)')
plt.axis('off')
plt.savefig(folder+"fur_log.png", bbox_inches='tight', pad_inches=0, dpi=DPI)
plt.close()

for i in range(len(g_k)):
    plt.figure(figsize=FIG_SIZE, dpi=DPI)
    ker = g_k[i]
    ker_appl(ker, gray, f"gauss_{N[i]}")
    fur_ker = scipy.fftshift(scipy.fft2(ker))
    magnitude = np.log1p(abs(fur_ker))
        
    plt.imshow(magnitude, cmap="gray")
    plt.axis('off')
    plt.savefig(folder+f"ker_gaus{N[i]}.png", bbox_inches='tight', pad_inches=0, dpi=DPI)
    plt.close()

for i in range(len(b_k)):
    plt.figure(figsize=FIG_SIZE, dpi=DPI)
    ker = b_k[i]
    ker_appl(ker, gray, f"block_{N[i]}")
    fur_ker = scipy.fftshift(scipy.fft2(ker))
    magnitude = np.log1p(abs(fur_ker))
        
    plt.imshow(magnitude, cmap="gray")
    plt.axis('off')
    plt.savefig(folder+f"ker_block{N[i]}.png", bbox_inches='tight', pad_inches=0, dpi=DPI)
    plt.close()

fur_ker = scipy.fftshift(scipy.fft2(K_s))
magnitude = np.log1p(abs(fur_ker))
ker_appl(K_s, gray, f"sharp")    
plt.figure(figsize=FIG_SIZE, dpi=DPI)
plt.imshow(magnitude, cmap="gray")
plt.axis('off')
plt.savefig(folder+f"ker_sharp.png", bbox_inches='tight', pad_inches=0, dpi=DPI)
plt.close()

fur_ker = scipy.fftshift(scipy.fft2(K_e))
magnitude = np.log1p(abs(fur_ker))
ker_appl(K_e, gray, f"edge")
plt.figure(figsize=FIG_SIZE, dpi=DPI)
plt.imshow(magnitude, cmap="gray")
plt.axis('off')
plt.savefig(folder+f"ker_edges.png", bbox_inches='tight', pad_inches=0, dpi=DPI)
plt.close()

for i in range(len(g_k)):
    ker = g_k[i]
    res = convolve2d(gray, ker, mode='same', boundary='fill', fillvalue=0)
    res_norm = cv2.normalize(res, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
    cv2.imwrite(folder+f"noita_gaus{N[i]}.png", res_norm)

for i in range(len(g_k)):
    ker = b_k[i]
    res = convolve2d(gray, ker, mode='same', boundary='fill', fillvalue=0)
    res_norm = cv2.normalize(res, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
    cv2.imwrite(folder+f"noita_block{N[i]}.png", res_norm)

res = convolve2d(gray, K_s, mode='same', boundary='fill', fillvalue=0)
res_norm = np.clip(res, 0, 255).astype(np.uint8)
cv2.imwrite(folder+f"noita_sharp.png", res_norm)

res = convolve2d(gray, K_e, mode='same', boundary='fill', fillvalue=0)
res_norm = np.clip(res, 0, 255).astype(np.uint8)
cv2.imwrite(folder+f"noita_edges.png", res_norm)