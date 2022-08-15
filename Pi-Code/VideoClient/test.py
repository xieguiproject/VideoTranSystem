src = '{"cmd":"getdata","size":"640*480","ys":"37"}{"cmd":"getdata","size":"640*480","ys":"36"}{"cmd":"getdata","size":"640*480","ys":"35"}{"cmd":"getdata","size":"640*480","ys":"39"}'
rst = src.split('}{')
if(len(rst) > 0):
    rst = '{' + rst[-1]
print(rst)
