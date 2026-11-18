"""Deterministic OpenCV image-to-coloring-page conversion."""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import cv2
import numpy as np

@dataclass(frozen=True, slots=True)
class ConversionOptions:
    max_dimension: int = 2400
    canny_low: int = 60
    canny_high: int = 150
    line_thickness: int = 1
    preserve_small_dark_details: bool = True
    small_detail_area_fraction: float = 0.0002
    min_component_area: int = 3
    use_color_edges: bool = False
    mean_shift_spatial_radius: int = 15
    mean_shift_color_radius: int = 35
    mean_shift_max_level: int = 1

    def __post_init__(self):
        if self.max_dimension < 0: raise ValueError("max_dimension must be >= 0")
        if not 0 <= self.canny_low < self.canny_high <= 255: raise ValueError("Invalid Canny thresholds")
        if self.line_thickness < 0: raise ValueError("line_thickness must be >= 0")
        if not 0 <= self.small_detail_area_fraction <= 0.01: raise ValueError("Invalid detail area fraction")
        if self.min_component_area < 1: raise ValueError("min_component_area must be >= 1")
        if min(self.mean_shift_spatial_radius,self.mean_shift_color_radius) < 1: raise ValueError("Mean-shift radii must be >= 1")
        if self.mean_shift_max_level < 0: raise ValueError("mean_shift_max_level must be >= 0")

def _as_bgr(image: np.ndarray) -> np.ndarray:
    if image.ndim == 2: return cv2.cvtColor(image,cv2.COLOR_GRAY2BGR)
    if image.ndim == 3 and image.shape[2] == 4:
        bgr=image[:,:,:3].astype(np.float32); alpha=image[:,:,3:4].astype(np.float32)/255.0
        return np.clip(bgr*alpha+255.0*(1.0-alpha),0,255).astype(np.uint8)
    if image.ndim == 3 and image.shape[2] == 3: return image
    raise ValueError(f"Unsupported image shape: {image.shape}")

def _edges(image: np.ndarray, options: ConversionOptions) -> np.ndarray:
    smooth=cv2.pyrMeanShiftFiltering(image,sp=options.mean_shift_spatial_radius,sr=options.mean_shift_color_radius,maxLevel=options.mean_shift_max_level)
    lab=cv2.cvtColor(smooth,cv2.COLOR_BGR2LAB)
    lum=cv2.GaussianBlur(lab[:,:,0],(3,3),0)
    edges=cv2.Canny(lum,options.canny_low,options.canny_high)
    if options.use_color_edges:
        for idx in (1,2):
            ch=cv2.GaussianBlur(lab[:,:,idx],(3,3),0)
            edges=cv2.bitwise_or(edges,cv2.Canny(ch,max(18,options.canny_low-12),max(70,options.canny_high-15)))
    return edges

def _preserve_dark_details(image: np.ndarray, edges: np.ndarray, options: ConversionOptions) -> np.ndarray:
    if not options.preserve_small_dark_details: return edges
    gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY); dark=cv2.inRange(gray,0,58)
    count,labels,stats,_=cv2.connectedComponentsWithStats(dark,connectivity=8)
    limit=max(4,int(image.shape[0]*image.shape[1]*options.small_detail_area_fraction)); result=edges.copy()
    for i in range(1,count):
        area=int(stats[i,cv2.CC_STAT_AREA])
        if 2 <= area <= limit: result[labels==i]=255
    return result

def _remove_tiny(edges: np.ndarray, minimum: int) -> np.ndarray:
    if minimum <= 1: return edges
    count,labels,stats,_=cv2.connectedComponentsWithStats(edges,connectivity=8)
    keep=np.zeros(count,dtype=np.uint8)
    for i in range(1,count):
        if int(stats[i,cv2.CC_STAT_AREA]) >= minimum: keep[i]=1
    return (keep[labels]*255).astype(np.uint8)

def convert_array(image: np.ndarray, options: ConversionOptions | None = None) -> np.ndarray:
    """Return single-channel binary black (0) and white (255) line art."""
    options=options or ConversionOptions()
    if not isinstance(image,np.ndarray) or image.size == 0: raise ValueError("image must be a non-empty NumPy array")
    work=_as_bgr(image.copy())
    if work.dtype != np.uint8: work=np.clip(work,0,255).astype(np.uint8)
    if options.max_dimension:
        h,w=work.shape[:2]; longest=max(h,w)
        if longest > options.max_dimension:
            scale=options.max_dimension/float(longest)
            work=cv2.resize(work,(max(1,round(w*scale)),max(1,round(h*scale))),interpolation=cv2.INTER_AREA)
    lines=_remove_tiny(_preserve_dark_details(work,_edges(work,options),options),options.min_component_area)
    kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
    lines=cv2.morphologyEx(lines,cv2.MORPH_CLOSE,kernel,iterations=1)
    if options.line_thickness: lines=cv2.dilate(lines,kernel,iterations=options.line_thickness)
    output=np.full(lines.shape,255,dtype=np.uint8); output[lines>0]=0
    return output

def convert_file(input_path: str | Path, output_path: str | Path, options: ConversionOptions | None = None) -> Path:
    """Convert an image file and write the resulting PNG/image."""
    source,destination=Path(input_path),Path(output_path)
    if not source.is_file(): raise FileNotFoundError(f"Input image does not exist: {source}")
    image=cv2.imread(str(source),cv2.IMREAD_UNCHANGED)
    if image is None: raise ValueError(f"Could not read image: {source}")
    result=convert_array(image,options); destination.parent.mkdir(parents=True,exist_ok=True)
    if not cv2.imwrite(str(destination),result): raise OSError(f"Could not write output image: {destination}")
    return destination
