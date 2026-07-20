#!/usr/bin/env python3
"""Generate the project-page figures from our measured numbers + maze images. Headless."""
import os, csv, random
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np
from PIL import Image, ImageDraw

WPR="/home/harshita/projects/wpr"
OUT="/home/harshita/projects/indoor-vpr-audit/static/images"
INK="#1f2430"; MUTED="#6b7280"; GRID="#e7e9ee"; MODEL="#2f6fb3"; CHANCE="#9aa0ab"
plt.rcParams.update({"font.size":12,"axes.edgecolor":"#c7ccd6","axes.linewidth":1.0,
                     "text.color":INK,"axes.labelcolor":INK,"xtick.color":MUTED,"ytick.color":MUTED,
                     "svg.fonttype":"none","figure.dpi":150})

# ---------- Fig 1: recall + shuffled floor vs GT radius, small DB vs big DB ----------
R=[10,15,20,25]
data={
 "Baidu — 689-image database":dict(real=[78.69,87.35,89.87,91.10], chance=[4.71,9.19,13.22,16.94]),
 "Baidu — 5,207-image database":dict(real=[77.84,84.05,86.76,87.75], chance=[1.21,2.58,3.82,5.40]),
}
fig,axes=plt.subplots(1,2,figsize=(10.5,4.3),sharey=True)
for ax,(title,d) in zip(axes,data.items()):
    ax.plot(R,d["real"],color=MODEL,lw=2.4,marker="o",ms=6,solid_capstyle="round",zorder=3)
    ax.plot(R,d["chance"],color=CHANCE,lw=2.2,marker="o",ms=5,linestyle=(0,(4,3)),solid_capstyle="round",zorder=2)
    ax.text(R[-1]+0.4,d["real"][-1],f" MegaLoc R@1\n {d['real'][-1]:.0f}",va="center",color=MODEL,fontsize=11,fontweight="bold")
    ax.text(R[-1]+0.4,d["chance"][-1]+3,f" shuffled\n floor {d['chance'][-1]:.0f}",va="center",color="#70757f",fontsize=10.5)
    ax.set_title(title,fontsize=12,color=INK,pad=8,loc="left")
    ax.set_xlabel("ground-truth radius  (metres)")
    ax.set_xticks(R); ax.set_xlim(9,29); ax.set_ylim(0,100)
    ax.grid(axis="y",color=GRID,lw=1); ax.set_axisbelow(True)
    for s in ("top","right"): ax.spines[s].set_visible(False)
axes[0].set_ylabel("Recall@1  (%)")
axes[1].annotate("= paper 87.7",(25,87.75),xytext=(20.2,64),color="#3a7d3a",fontsize=10.5,
                 arrowprops=dict(arrowstyle="-",color="#8fbf8f",lw=1.2))
fig.suptitle("Recall and the shuffled-retriever floor both rise with the GT radius — and the floor rises far\nfaster on a small database",
             x=0.02,ha="left",fontsize=13.5,fontweight="bold",color=INK)
fig.tight_layout(rect=[0,0,1,0.9])
fig.savefig(f"{OUT}/fig_fragility.png",bbox_inches="tight",facecolor="white")
print("saved fig_fragility.png")

# ---------- Fig 2: clean vs masked maze examples ----------
rows=list(csv.DictReader(open(f"{WPR}/data/maze/out/maze_mask_stats.csv")))
for r in rows: r["lcf"]=float(r["largest_component_frac"])
random.seed(3)
fol={"db":"database","query":"queries"}
clean=random.sample([r for r in rows if r["lcf"]<0.002],4)
masked=random.sample([r for r in rows if r["lcf"]>0.18],4)
cols,tw,th=4,300,210
cv=Image.new("RGB",(cols*tw, 2*th+56),"white"); d=ImageDraw.Draw(cv)
d.text((10,8),"maze — CLEAN (no masking)",fill=(40,120,60))
d.text((10,th+40),"maze — MASKED (baked white silhouette)",fill=(180,50,50))
for row,(items,col) in enumerate([(clean,(40,150,70)),(masked,(200,60,60))]):
    y0=28+row*(th+18)
    for ci,r in enumerate(items):
        im=Image.open(f"{WPR}/data/maze/images/test/{fol[r['subset']]}/{r['filename']}").convert("RGB")
        im.thumbnail((tw-14,th-28)); x=ci*tw
        cv.paste(im,(x+7,y0+22)); d.rectangle([x+5,y0+20,x+tw-2,y0+th-2],outline=col,width=3)
        d.text((x+9,y0+4),f"lcf={r['lcf']:.3f}",fill=col)
cv.save(f"{OUT}/fig_mask_examples.png"); print("saved fig_mask_examples.png")
print("done")
