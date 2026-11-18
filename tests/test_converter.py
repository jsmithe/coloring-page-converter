from __future__ import annotations
import cv2
import numpy as np
import pytest
from coloring_page_converter import ConversionOptions, convert_array, convert_file

def sample_illustration():
    image=np.full((180,240,3),255,dtype=np.uint8)
    cv2.rectangle(image,(25,25),(215,155),(30,120,220),thickness=-1)
    cv2.circle(image,(90,85),32,(40,190,90),thickness=-1)
    cv2.circle(image,(82,78),4,(0,0,0),thickness=-1)
    cv2.circle(image,(98,78),4,(0,0,0),thickness=-1)
    cv2.line(image,(0,170),(239,170),(0,0,0),thickness=3)
    return image

def test_output_is_binary_black_and_white():
    result=convert_array(sample_illustration())
    assert result.dtype == np.uint8 and result.ndim == 2
    assert set(np.unique(result)).issubset({0,255})
    assert 0 in np.unique(result) and 255 in np.unique(result)

def test_resize_respects_max_dimension():
    image=np.full((400,800,3),255,dtype=np.uint8)
    assert convert_array(image,ConversionOptions(max_dimension=300)).shape == (150,300)

def test_grayscale_input_is_supported():
    image=np.full((60,80),255,dtype=np.uint8); cv2.rectangle(image,(10,10),(70,50),0,thickness=2)
    result=convert_array(image)
    assert result.shape == image.shape and 0 in np.unique(result)

def test_invalid_thresholds_are_rejected():
    with pytest.raises(ValueError): ConversionOptions(canny_low=150,canny_high=100)

def test_convert_file_writes_png(tmp_path):
    source=tmp_path/"input.png"; output=tmp_path/"nested"/"output.png"
    assert cv2.imwrite(str(source),sample_illustration())
    assert convert_file(source,output) == output
    saved=cv2.imread(str(output),cv2.IMREAD_GRAYSCALE)
    assert saved is not None and saved.shape == (180,240)
    assert set(np.unique(saved)).issubset({0,255})

def test_transparent_input_is_composited_on_white():
    image=np.zeros((40,40,4),dtype=np.uint8); image[:,:,:3]=(0,0,0); image[:,:,3]=0
    cv2.rectangle(image,(10,10),(30,30),(0,0,0,255),thickness=2)
    result=convert_array(image)
    assert result.shape == (40,40) and result[0,0] == 255 and 0 in np.unique(result)

def test_empty_input_is_rejected():
    with pytest.raises(ValueError): convert_array(np.array([],dtype=np.uint8))
