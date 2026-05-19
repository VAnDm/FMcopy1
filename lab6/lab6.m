im = imread('7.png');
im2 = double(im) / 255;
fur_im = fftshift(fft2(im2));
mods = abs(fur_im);
angles = angle(fur_im);
mods_log = log(mods + 1);
max_mods_log = max(mods_log,[],'all');
min_mods_log = min(mods_log,[],'all');
mods_img = (mods_log - min_mods_log) / (max_mods_log - min_mods_log);
%imwrite(mods_img, "furie.png")
fur_fil_raw = imread('furie_fil.png');
fur_fil = double(fur_fil_raw) / 255;
fur_fil_mod = exp((fur_fil * (max_mods_log - min_mods_log) + min_mods_log)) - 1; 
fur_fil_res = exp(1i * angles) .* fur_fil_mod;
im_fil = ifft2(ifftshift(fur_fil_res));
imwrite(im_fil, "filtered.png");




