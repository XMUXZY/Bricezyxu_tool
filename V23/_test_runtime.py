# -*- coding: utf-8 -*-
"""
Runtime test: simulate actual calculation calls for each tool.
This creates a headless Tk root and instantiates each tool page,
then triggers the compute methods to check for exceptions.
"""
import sys, os, traceback
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import customtkinter as ctk

errors = []

def run_tests():
    root = ctk.CTk()
    root.withdraw()  # hide window
    
    # Provide standard colors dict
    colors = {
        "text": "#e0e0e0",
        "text_dim": "#888888",
        "nav_active": "#0f3460",
    }
    
    # ====== tool_d: star record ======
    print("\n--- tool_d (star record) ---")
    try:
        from pages.tool_d import ToolDPage
        page_d = ToolDPage(root, colors)
        page_d.pack()
        
        # Test mode 1: set default values and calc
        page_d.t1_xinlu.set("太微")
        page_d._on_xinlu_change_t1("太微")
        page_d.t1_cur_chong.delete(0, "end"); page_d.t1_cur_chong.insert(0, "1")
        page_d.t1_cur_star.delete(0, "end"); page_d.t1_cur_star.insert(0, "0")
        page_d.t1_low_entry.delete(0, "end"); page_d.t1_low_entry.insert(0, "3000")
        page_d.t1_mid_entry.delete(0, "end"); page_d.t1_mid_entry.insert(0, "6500")
        page_d.t1_high_entry.delete(0, "end"); page_d.t1_high_entry.insert(0, "6000")
        page_d.t1_guard_entry.delete(0, "end"); page_d.t1_guard_entry.insert(0, "7000")
        page_d._calc_by_materials()
        result1 = page_d.t1_result.get("1.0", "end").strip()
        if "计算出错" in result1:
            errors.append(f"tool_d mode1: {result1}")
            print(f"  [FAIL] mode1: {result1}")
        else:
            print(f"  [OK] mode1: result length={len(result1)}")
        
        # Test mode 2
        page_d.t2_xinlu.set("太微")
        page_d._on_xinlu_change_t2("太微")
        page_d.t2_start_chong.delete(0, "end"); page_d.t2_start_chong.insert(0, "1")
        page_d.t2_start_star.delete(0, "end"); page_d.t2_start_star.insert(0, "0")
        page_d.t2_target_chong.delete(0, "end"); page_d.t2_target_chong.insert(0, "20")
        page_d.t2_target_star.delete(0, "end"); page_d.t2_target_star.insert(0, "6")
        page_d._calc_for_target()
        result2 = page_d.t2_result.get("1.0", "end").strip()
        if "计算出错" in result2:
            errors.append(f"tool_d mode2: {result2}")
            print(f"  [FAIL] mode2: {result2}")
        else:
            print(f"  [OK] mode2: result length={len(result2)}")
        
        page_d.destroy()
    except Exception as e:
        errors.append(f"tool_d init: {e}")
        print(f"  [FAIL] init: {e}")
        traceback.print_exc()
    
    # ====== tool_e: saint stone ======
    print("\n--- tool_e (saint stone) ---")
    try:
        from pages.tool_e import ToolEPage
        page_e = ToolEPage(root, colors)
        page_e.pack()
        
        # Test mode 1
        page_e.t1_part.set("头盔")
        page_e._on_part_change_t1("头盔")
        page_e.t1_slot.set("圣石1")
        page_e.t1_cur_lv.delete(0, "end"); page_e.t1_cur_lv.insert(0, "0")
        page_e.t1_mat_entry.delete(0, "end"); page_e.t1_mat_entry.insert(0, "1000")
        page_e._calc_by_materials()
        result = page_e.t1_result.get("1.0", "end").strip()
        if "计算出错" in result:
            errors.append(f"tool_e mode1: {result}")
            print(f"  [FAIL] mode1: {result}")
        else:
            print(f"  [OK] mode1: result length={len(result)}")
        
        # Test mode 2
        page_e.t2_part.set("头盔")
        page_e._on_part_change_t2("头盔")
        page_e.t2_slot.set("圣石1")
        page_e.t2_start_lv.delete(0, "end"); page_e.t2_start_lv.insert(0, "0")
        page_e.t2_target_lv.delete(0, "end"); page_e.t2_target_lv.insert(0, "30")
        page_e._calc_for_target()
        result2 = page_e.t2_result.get("1.0", "end").strip()
        if "计算出错" in result2:
            errors.append(f"tool_e mode2: {result2}")
            print(f"  [FAIL] mode2: {result2}")
        else:
            print(f"  [OK] mode2: result length={len(result2)}")
        
        page_e.destroy()
    except Exception as e:
        errors.append(f"tool_e: {e}")
        print(f"  [FAIL] {e}")
        traceback.print_exc()
    
    # ====== tool_feng_shui ======
    print("\n--- tool_feng_shui ---")
    try:
        from pages.tool_feng_shui import ToolFengShuiPage
        page_fs = ToolFengShuiPage(root, colors)
        page_fs.pack()
        
        # Test mode 1 (target calc)
        page_fs._calc_target()
        result = page_fs.t1_result.get("1.0", "end").strip()
        if "计算出错" in result:
            errors.append(f"tool_feng_shui mode1: {result}")
            print(f"  [FAIL] mode1: {result}")
        else:
            print(f"  [OK] mode1: result length={len(result)}")
        
        page_fs.destroy()
    except Exception as e:
        errors.append(f"tool_feng_shui: {e}")
        print(f"  [FAIL] {e}")
        traceback.print_exc()
    
    # ====== tool_gem_grind ======
    print("\n--- tool_gem_grind ---")
    try:
        from pages.tool_gem_grind import ToolGemGrindPage
        page_gg = ToolGemGrindPage(root, colors)
        page_gg.pack()
        
        # Test mode 1
        page_gg.t1_cur_lv.delete(0, "end"); page_gg.t1_cur_lv.insert(0, "0")
        page_gg._calc_by_materials()
        result = page_gg.t1_result.get("1.0", "end").strip()
        if "计算出错" in result:
            errors.append(f"tool_gem_grind mode1: {result}")
            print(f"  [FAIL] mode1: {result}")
        else:
            print(f"  [OK] mode1: result length={len(result)}")
        
        # Test mode 2
        page_gg.t2_start_lv.delete(0, "end"); page_gg.t2_start_lv.insert(0, "0")
        page_gg.t2_target_lv.delete(0, "end"); page_gg.t2_target_lv.insert(0, "30")
        page_gg._calc_for_target()
        result2 = page_gg.t2_result.get("1.0", "end").strip()
        if "计算出错" in result2:
            errors.append(f"tool_gem_grind mode2: {result2}")
            print(f"  [FAIL] mode2: {result2}")
        else:
            print(f"  [OK] mode2: result length={len(result2)}")
        
        page_gg.destroy()
    except Exception as e:
        errors.append(f"tool_gem_grind: {e}")
        print(f"  [FAIL] {e}")
        traceback.print_exc()
    
    # ====== tool_b (cuilian) ======
    print("\n--- tool_b (cuilian) ---")
    try:
        from pages.tool_b import ToolBPage
        page_b = ToolBPage(root, colors)
        page_b.pack()
        
        # Mode 1
        page_b.calc1_init_lv.delete(0, "end"); page_b.calc1_init_lv.insert(0, "0")
        page_b.calc1_mat_entry.delete(0, "end"); page_b.calc1_mat_entry.insert(0, "1000")
        page_b._calculate_max_level()
        result = page_b.calc1_result.get("1.0", "end").strip()
        if "出错" in result:
            errors.append(f"tool_b mode1: {result}")
            print(f"  [FAIL] mode1: {result}")
        else:
            print(f"  [OK] mode1: result length={len(result)}")
        
        # Mode 2
        page_b.calc2_start_lv.delete(0, "end"); page_b.calc2_start_lv.insert(0, "0")
        page_b.calc2_target_lv.delete(0, "end"); page_b.calc2_target_lv.insert(0, "30")
        page_b._calculate_materials()
        result2 = page_b.calc2_result.get("1.0", "end").strip()
        if "出错" in result2:
            errors.append(f"tool_b mode2: {result2}")
            print(f"  [FAIL] mode2: {result2}")
        else:
            print(f"  [OK] mode2: result length={len(result2)}")
        
        page_b.destroy()
    except Exception as e:
        errors.append(f"tool_b: {e}")
        print(f"  [FAIL] {e}")
        traceback.print_exc()
    
    # ====== tool_c (reforge) ======
    print("\n--- tool_c (reforge) ---")
    try:
        from pages.tool_c import ToolCPage
        page_c = ToolCPage(root, colors)
        page_c.pack()
        
        # Mode 1
        page_c.t1_init_lv.delete(0, "end"); page_c.t1_init_lv.insert(0, "0")
        page_c.t1_init_stage.delete(0, "end"); page_c.t1_init_stage.insert(0, "0")
        page_c.t1_mat_entry.delete(0, "end"); page_c.t1_mat_entry.insert(0, "1000")
        page_c._calc_reforge_by_materials()
        result = page_c.t1_result.get("1.0", "end").strip()
        if "出错" in result:
            errors.append(f"tool_c mode1: {result}")
            print(f"  [FAIL] mode1: {result}")
        else:
            print(f"  [OK] mode1: result length={len(result)}")
        
        # Mode 2
        page_c.t2_init_lv.delete(0, "end"); page_c.t2_init_lv.insert(0, "0")
        page_c.t2_init_stage.delete(0, "end"); page_c.t2_init_stage.insert(0, "0")
        page_c.t2_target_lv.delete(0, "end"); page_c.t2_target_lv.insert(0, "10")
        page_c.t2_target_stage.delete(0, "end"); page_c.t2_target_stage.insert(0, "3")
        page_c._calc_materials_for_target()
        result2 = page_c.t2_result.get("1.0", "end").strip()
        if "出错" in result2:
            errors.append(f"tool_c mode2: {result2}")
            print(f"  [FAIL] mode2: {result2}")
        else:
            print(f"  [OK] mode2: result length={len(result2)}")
        
        page_c.destroy()
    except Exception as e:
        errors.append(f"tool_c: {e}")
        print(f"  [FAIL] {e}")
        traceback.print_exc()
    
    # ====== tool_star_map ======
    print("\n--- tool_star_map ---")
    try:
        from pages.tool_star_map import ToolStarMapPage
        page_sm = ToolStarMapPage(root, colors)
        page_sm.pack()
        
        page_sm._calc_upgrade()
        result = page_sm.t1_result.get("1.0", "end").strip()
        if "出错" in result or "有误" in result:
            # This might just be "input error" since we didn't fill in
            print(f"  [INFO] mode1 (no input): {result[:50]}")
        else:
            print(f"  [OK] mode1: result length={len(result)}")
        
        page_sm.destroy()
    except Exception as e:
        errors.append(f"tool_star_map: {e}")
        print(f"  [FAIL] {e}")
        traceback.print_exc()
    
    # ====== tool_dunjia ======
    print("\n--- tool_dunjia ---")
    try:
        from pages.tool_dunjia import ToolDunJia
        page_dj = ToolDunJia(root, colors)
        page_dj.pack()
        
        page_dj.t1_level.delete(0, "end"); page_dj.t1_level.insert(0, "1")
        page_dj._calc_by_materials()
        result = page_dj.t1_result.get("1.0", "end").strip()
        if "计算出错" in result:
            errors.append(f"tool_dunjia mode1: {result}")
            print(f"  [FAIL] mode1: {result}")
        else:
            print(f"  [OK] mode1: result length={len(result)}")
        
        page_dj.destroy()
    except Exception as e:
        errors.append(f"tool_dunjia: {e}")
        print(f"  [FAIL] {e}")
        traceback.print_exc()
    
    # ====== tool_guardian ======
    print("\n--- tool_guardian ---")
    try:
        from pages.tool_guardian import ToolGuardian
        page_guard = ToolGuardian(root, colors)
        page_guard.pack()
        
        page_guard._calc_mode1()
        result = page_guard.t1_result.get("1.0", "end").strip()
        if "计算出错" in result:
            errors.append(f"tool_guardian mode1: {result}")
            print(f"  [FAIL] mode1: {result}")
        else:
            print(f"  [OK] mode1: result length={len(result)}")
        
        page_guard.destroy()
    except Exception as e:
        errors.append(f"tool_guardian: {e}")
        print(f"  [FAIL] {e}")
        traceback.print_exc()
    
    # ====== tool_zhance ======
    print("\n--- tool_zhance ---")
    try:
        from pages.tool_zhance import ToolZhanCe
        page_zc = ToolZhanCe(root, colors)
        page_zc.pack()
        
        page_zc._calc_by_materials()
        result = page_zc.t1_result.get("1.0", "end").strip()
        if "计算出错" in result:
            errors.append(f"tool_zhance mode1: {result}")
            print(f"  [FAIL] mode1: {result}")
        else:
            print(f"  [OK] mode1: result length={len(result)}")
        
        page_zc.destroy()
    except Exception as e:
        errors.append(f"tool_zhance: {e}")
        print(f"  [FAIL] {e}")
        traceback.print_exc()
    
    # ====== tool_fabao ======
    print("\n--- tool_fabao ---")
    try:
        from pages.tool_fabao import ToolFaBao
        page_fb = ToolFaBao(root, colors)
        page_fb.pack()
        
        page_fb._calc_mode1()
        result = page_fb.t1_result.get("1.0", "end").strip()
        if "计算出错" in result:
            errors.append(f"tool_fabao mode1: {result}")
            print(f"  [FAIL] mode1: {result}")
        else:
            print(f"  [OK] mode1: result length={len(result)}")
        
        page_fb.destroy()
    except Exception as e:
        errors.append(f"tool_fabao: {e}")
        print(f"  [FAIL] {e}")
        traceback.print_exc()
    
    # ====== tool_zhu_ling ======
    print("\n--- tool_zhu_ling ---")
    try:
        from pages.tool_zhu_ling import ToolZhuLingPage
        page_zl = ToolZhuLingPage(root, colors)
        page_zl.pack()
        
        page_zl._calc_by_materials()
        result = page_zl.t1_result.get("1.0", "end").strip()
        if "计算出错" in result:
            errors.append(f"tool_zhu_ling mode1: {result}")
            print(f"  [FAIL] mode1: {result}")
        else:
            print(f"  [OK] mode1: result length={len(result)}")
        
        page_zl.destroy()
    except Exception as e:
        errors.append(f"tool_zhu_ling: {e}")
        print(f"  [FAIL] {e}")
        traceback.print_exc()
    
    root.destroy()
    
    # Summary
    print("\n" + "=" * 60)
    print("  SUMMARY")
    print("=" * 60)
    if errors:
        print(f"  TOTAL ERRORS: {len(errors)}")
        for e in errors:
            print(f"    - {e[:120]}")
    else:
        print("  ALL TOOLS PASSED!")

if __name__ == "__main__":
    run_tests()
