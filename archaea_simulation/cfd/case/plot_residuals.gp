# Set terminal to PNG
set terminal pngcairo enhanced color font 'Arial,10' size 800, 600
set output 'residuals.png'
set title "Residuals per Iteration"
set xlabel "Iteration"
set ylabel "Residual"
set grid
plot "./postProcessing/residuals/0/residuals.dat" using 1:3 with lines title 'Ux', \
     "./postProcessing/residuals/0/residuals.dat" using 1:4 with lines title 'Uy', \
     "./postProcessing/residuals/0/residuals.dat" using 1:5 with lines title 'Uz', \
     "./postProcessing/residuals/0/residuals.dat" using 1:6 with lines title 'p'

# Set terminal to SVG for vector graphics output
set terminal svg size 800, 600 fname 'Arial' fsize 10
set output 'residuals.svg'
replot

