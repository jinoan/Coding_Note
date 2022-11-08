def iou(gt_bbox, pred_bbox, bbox_format='xyxy'):
    if bbox_format == 'xyxy':
        gx0, gy0, gx1, gy1 = gt_bbox
        px0, py0, px1, py1 = pred_bbox
        gw = gx1 - gx0
        gh = gy1 - gy0
        pw = px1 - px0
        ph = py1 - py0
    elif bbox_format == 'xywh':
        gx, gy, gw, gh = gt_bbox
        px, py, pw, ph = pred_bbox
        gx0 = gx - gw / 2
        gy0 = gy - gh / 2
        gx1 = gx + gw / 2
        gy1 = gy + gh / 2
        px0 = px - pw / 2
        py0 = py - ph / 2
        px1 = px + pw / 2
        py1 = py + ph / 2
    else:
        raise ValueError("The parameter 'bbox_format' value must be 'xyxy' or 'xywh'.")
    
    ix0 = max(gx0, px0)
    ix1 = min(gx1, px1)
    iy0 = max(gy0, py0)
    iy1 = min(gy1, py1)
    iw = ix1 - ix0
    ih - iy1 - iy0

    if iw <= 0 or ih <= 0:
        return 0

    I = iw * ih  # interaction
    U = gw * gh + pw * ph  # union

    return I / U
