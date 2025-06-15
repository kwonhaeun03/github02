# 넙스리본, 폴리클 조인트까지 만들고 아웃라이너 정리 후 과정

## 0, 0, 0 위치에 조인트 여러개 생성하는 코드 (parent 안된상태로)

import maya.cmds as cmds

cmds.select(cl=1)

part_list = ['up', 'low']
physical_list = ['leg', 'arm']
side_list = ['L0', 'R0']

# 조인트 이름 패턴 생성 및 반복문으로 조인트 생성
# 왼쪽 조인트 생성
for side in side_list:
    for part in part_list:
        for section in physical_list:
            for i in range(1, 8):  # 1부터 7까지 반복
                name = f"{section}_{side}_{part}_folliclejoint{i}"  # f-string으로 이름 생성
                cmds.joint(n=name)
                cmds.select(cl=1)  # 선택 해제

## 조인트들을 follicle 안으로 각각 parent 시키는 코드
# 정확한 follicle 번호 리스트
follicle_numbers = [50, 1750, 3350, 5050, 6650, 8350, 9950]

part_list = ['up', 'low']
physical_list = ['leg', 'arm']
side_list = ['L0', 'R0']

# 반복문으로 parent 작업 수행
# 왼쪽 작업
for side in side_list:
    for part in part_list:
        for section in physical_list:
            for i, follicle in enumerate(follicle_numbers, start=1):
                cmds.parent(f"{section}_{side}_{part}_folliclejoint{i}", f"{section}_{side}_{part}_twist_ribFollicle{follicle}")

## 폴리클 안에 넣은 조인트들을 0, 0, 0, 0, 0, 0 로 바꾸는 코드

cmds.select(cl=1)

for side in side_list:
    for part in part_list:
        for section in physical_list:
            for i in range(1, 8):  # 1부터 7까지 반복
                name = f"{section}_{side}_{part}_folliclejoint{i}"
                for axis in ['X', 'Y', 'Z']:  # X, Y, Z 한번씩
                    cmds.setAttr(f"{name}.translate{axis}", 0)
                    cmds.setAttr(f"{name}.rotate{axis}", 0)
            
# 2(L, R 방향)*2(섹션)*2(파트)*7(조인트 수)*3(X, Y, Z)*2(translate, rotate)=336 총 336개의 명령 처리

## 제 위치로 이동한 조인트들을 포지션값을 유지할 pos 그룹짓는 코드

cmds.select(cl=1)

for side in side_list:
    for part in part_list:
        for section in physical_list:
            for i in range(1, 8):  # 1부터 7까지 반복
                name = f"{section}_{side}_{part}_folliclejoint{i}"
                name_pos = f"{name}_pos"
                parent_node = cmds.createNode("transform", name=name_pos)
                cmds.select(cl=1)
                follicle = cmds.listRelatives(name, parent=1)[0]
                cmds.matchTransform(parent_node, name)
                cmds.parent(parent_node, follicle)
                cmds.parent(name, parent_node)
                cmds.select(cl=1)

## maintain offset=False인 point constrain 과 orient constrain을 이용해 리본_pos 그룹을 정확한 위치에 가져다두는 코드

for side in side_list:
    poi_con_no = cmds.pointConstraint(f'arm_{side}_shoulder_main_loc', f'arm_{side}_elbow_main_loc', f'arm_{side}_up_twist_rib_pos', mo=False, weight=1)
    cmds.delete(poi_con_no)
    cmds.select(cl=1)

for side in side_list:
    ori_con_no = cmds.orientConstraint(f'arm_{side}_shoulder_main_loc', f'arm_{side}_up_twist_rib_pos', mo=False, weight=1)
    cmds.delete(ori_con_no)
    cmds.select(cl=1)

for side in side_list:
    poi_con_no = cmds.pointConstraint(f'arm_{side}_elbow_main_loc', f'arm_{side}_wrist_main_loc', f'arm_{side}_low_twist_rib_pos', mo=False, weight=1)
    cmds.delete(poi_con_no)
    cmds.select(cl=1)

for side in side_list:
    ori_con_no = cmds.orientConstraint(f'arm_{side}_elbow_main_loc', f'arm_{side}_low_twist_rib_pos', mo=False, weight=1)
    cmds.delete(ori_con_no)
    cmds.select(cl=1)

for side in side_list:
    poi_con_no = cmds.pointConstraint(f'leg_{side}_hip_main_loc', f'leg_{side}_knee_main_loc', f'leg_{side}_up_twist_rib_pos', mo=False, weight=1)
    cmds.delete(poi_con_no)
    cmds.select(cl=1)

for side in side_list:
    ori_con_no = cmds.orientConstraint(f'leg_{side}_hip_main_loc', f'leg_{side}_up_twist_rib_pos', mo=False, weight=1)
    cmds.delete(ori_con_no)
    cmds.select(cl=1)

for side in side_list:
    poi_con_no = cmds.pointConstraint(f'leg_{side}_knee_main_loc', f'leg_{side}_foot_main_loc', f'leg_{side}_low_twist_rib_pos', mo=False, weight=1)
    cmds.delete(poi_con_no)
    cmds.select(cl=1)

for side in side_list:
    ori_con_no = cmds.orientConstraint(f'leg_{side}_knee_main_loc', f'leg_{side}_low_twist_rib_pos', mo=False, weight=1)
    cmds.delete(ori_con_no)
    cmds.select(cl=1)

cmds.select(cl=1)

## follicle 안에있는 그룹들을 복제해서 hairSystem()Follicles 안에 넣고 복제하면서 생긴 이름 마지막의 1을 지운 후 _L_pos 를 _L_rb_pos로 rename하고 그 하위에있는 조인트도 끝에 _rb를 붙여 rename한다

part_list = ['up', 'low']
physical_list = ['leg', 'arm']
side_list = ['L0', 'R0']

cmds.select(cl=1)

for side in side_list:
    for part in part_list:
        for section in physical_list:
            for i in range(1, 8):  # 1부터 7까지 반복
                name = f"{section}_{side}_{part}_folliclejoint{i}"
                name_pos = f"{name}_pos"
                parent_node0 = cmds.createNode("transform", name=f"{name}_rb_pos")
                parent_node1 = cmds.createNode("transform", name=f"{name}_rb_poi")
                parent_node1_1 = cmds.createNode("transform", name=f"{name}_rb_rot")
                parent_node2 = cmds.createNode("transform", name=f"{name}_rb_par")
                cmds.select(cl=1)
                duplicated_jnt = cmds.joint(n=f'{name}_rb')
                cmds.select(cl=1)
                follicle = cmds.listRelatives(name_pos, parent=1)[0]
                follicle_grp = cmds.listRelatives(follicle, parent=1)[0]
                cmds.matchTransform(parent_node0, name_pos)
                cmds.matchTransform(parent_node1, name_pos)
                cmds.matchTransform(parent_node1_1, name_pos)
                cmds.matchTransform(parent_node2, name_pos)
                cmds.parent(parent_node0, follicle_grp)
                cmds.parent(parent_node1, parent_node0)
                cmds.parent(parent_node1_1, parent_node1)
                cmds.parent(parent_node2, parent_node1_1)
                cmds.parent(duplicated_jnt, parent_node2)
                cmds.select(cl=1)
                for axis in ['X', 'Y', 'Z']:  # X, Y, Z 한번씩
                    cmds.setAttr(f"{duplicated_jnt}.translate{axis}", 0)
                    cmds.setAttr(f"{duplicated_jnt}.rotate{axis}", 0)
                    cmds.setAttr(f"{duplicated_jnt}.jointOrient{axis}", 0)

## 트위스트 컨트롤러 만들고 제위치에 갖다두는 코드

cmds.select(cl=1)

for side in side_list:
    for part in part_list:
        for section in physical_list:
            ctl = cmds.circle(r=1, ch=0, n=f'{section}_{side}_{part}_twist_ctl')[0]
            cmds.select(cl=1)
            ctl_pos = f'{ctl}_pos'
            ctl_poi = f'{ctl}_poi'
            ctl_aim = f'{ctl}_aim'
            ctl_mul = f'{ctl}_mul'
            A = cmds.createNode("transform", name=ctl_pos)
            B = cmds.createNode("transform", name=ctl_poi)
            C = cmds.createNode("transform", name=ctl_aim)
            D = cmds.createNode("transform", name=ctl_mul)
            cmds.parent(B, A)
            cmds.parent(C, B)
            cmds.parent(D, C)
            cmds.parent(ctl, D)
            cmds.matchTransform(A, f'{section}_{side}_{part}_twist_rib_pos')

## 추후 트위스크 컨트롤러의 축을 보조로 잡아주는 null만들고 위치 잡아준 후 조인트 하위 로케이터 안으로 페어런트

for side in side_list:
    for part in part_list:
        for section in physical_list:
            A = cmds.createNode("transform", name=f'{section}_{side}_{part}_twist_null')
            cmds.matchTransform(A, f'{section}_{side}_{part}_twist_rib_pos')

for side in side_list:
    cmds.parent(f'arm_{side}_up_twist_null', f'arm_{side}_shoulder_main_loc')

for side in side_list:
    cmds.parent(f'arm_{side}_low_twist_null', f'arm_{side}_elbow_main_loc')

for side in side_list:
    cmds.parent(f'leg_{side}_up_twist_null', f'leg_{side}_hip_main_loc')

for side in side_list:
    cmds.parent(f'leg_{side}_low_twist_null', f'leg_{side}_knee_main_loc')

# 제 위치에서 많이 벗어나도 오류가 나지 않도록 많이 translate 9000으로 잡아주기 

for side in side_list:
    for part in part_list:
        for section in physical_list:
            cmds.setAttr(f"{section}_{side}_{part}_twist_null.translateY", 9000)

# 그냥 함수로 만들어도 되지만 컨스트레인들을 맞추고 다시 지워야하기때문에 반환이 필요해서 return 사용
def poi_con0_2(parent_1, parent_2, child, weight):
    return cmds.pointConstraint(parent_1, parent_2, child, mo=False, weight=weight)

def poi_con0_2_R(parent_2, parent_1, child, weight):
    return cmds.pointConstraint(parent_1, parent_2, child, mo=False, weight=weight)

def ori_con0(parent, child, weight):
    return cmds.orientConstraint(parent, child, mo=False, weight=weight)

def ori_con1(parent, child, weight):
    return cmds.orientConstraint(parent, child, mo=True, weight=weight)

def par_con1(parent, child, weight):
    return cmds.parentConstraint(parent, child, mo=True, weight=weight)


## 컨트롤러 위치 항상 관절 사이 중앙에 오도록 pointConstraint걸고 상위관절 바라보도록 aimConstraint하는 코드

section = 'arm'
part_list = ['shoulder', 'elbow', 'wrist']
parent_list=[]

#왼쪽 상부 하부에 mo=False인 상태로 pointConstraint
side = 'L0'

for part in part_list:
    parent_list.append(f'{section}_{side}_{part}_main_loc')

poi_con0_2(parent_list[0], parent_list[1], f'{section}_{side}_up_twist_ctl_poi', 1)
poi_con0_2(parent_list[1], parent_list[2], f'{section}_{side}_low_twist_ctl_poi', 1)

side = 'R0'
parent_list=[]

for part in part_list:
    parent_list.append(f'{section}_{side}_{part}_main_loc')

poi_con0_2(parent_list[0], parent_list[1], f'{section}_{side}_up_twist_ctl_poi', 1)
poi_con0_2(parent_list[1], parent_list[2], f'{section}_{side}_low_twist_ctl_poi', 1)

# aimConstraint 그냥걸면 로테이트시 헛돌기때문에 보조축 설정해서 연결
# 왼쪽
cmds.aimConstraint(
    'arm_L0_shoulder_main_loc',  # 타겟 오브젝트
    'arm_L0_up_twist_ctl_aim',  # 소스 오브젝트
    aimVector=[-1, 0, 0],  # aim 벡터
    upVector=[0, 1, 0],   # 업 벡터
    worldUpType="object",  # 월드 업 타입
    worldUpObject="arm_L0_up_twist_null",  # 월드 업 오브젝트
    mo=True
)

cmds.aimConstraint(
    'arm_L0_elbow_main_loc',  # 타겟 오브젝트
    'arm_L0_low_twist_ctl_aim',  # 소스 오브젝트
    aimVector=[-1, 0, 0],  # aim 벡터
    upVector=[0, 1, 0],   # 업 벡터
    worldUpType="object",  # 월드 업 타입
    worldUpObject="arm_L0_low_twist_null",  # 월드 업 오브젝트
    mo=True
)

# 오른쪽
cmds.aimConstraint(
    'arm_R0_shoulder_main_loc',  # 타겟 오브젝트
    'arm_R0_up_twist_ctl_aim',  # 소스 오브젝트
    aimVector=[1, 0, 0],  # aim 벡터
    upVector=[0, 1, 0],   # 업 벡터
    worldUpType="object",  # 월드 업 타입
    worldUpObject="arm_R0_up_twist_null",  # 월드 업 오브젝트
    mo=True
)

cmds.aimConstraint(
    'arm_R0_elbow_main_loc',  # 타겟 오브젝트
    'arm_R0_low_twist_ctl_aim',  # 소스 오브젝트
    aimVector=[-1, 0, 0],  # aim 벡터
    upVector=[0, 1, 0],   # 업 벡터
    worldUpType="object",  # 월드 업 타입
    worldUpObject="arm_R0_low_twist_null",  # 월드 업 오브젝트
    mo=True
)

cmds.select(cl=1)

section = 'leg'
part_list = ['hip', 'knee', 'foot']
parent_list=[]

side = 'L0'

for part in part_list:
    parent_list.append(f'{section}_{side}_{part}_main_loc')

poi_con0_2(parent_list[0], parent_list[1], f'{section}_{side}_up_twist_ctl_poi', 1)
poi_con0_2(parent_list[1], parent_list[2], f'{section}_{side}_low_twist_ctl_poi', 1)

side = 'R0'
parent_list=[]

for part in part_list:
    parent_list.append(f'{section}_{side}_{part}_main_loc')

poi_con0_2(parent_list[0], parent_list[1], f'{section}_{side}_up_twist_ctl_poi', 1)
poi_con0_2(parent_list[1], parent_list[2], f'{section}_{side}_low_twist_ctl_poi', 1)

# 왼쪽
cmds.aimConstraint(
    'leg_L0_hip_main_loc',  # 타겟 오브젝트
    'leg_L0_up_twist_ctl_aim',  # 소스 오브젝트
    aimVector=[-1, 0, 0],  # aim 벡터
    upVector=[0, 1, 0],   # 업 벡터
    worldUpType="object",  # 월드 업 타입
    worldUpObject="leg_L0_up_twist_null",  # 월드 업 오브젝트
    mo=True
)

cmds.aimConstraint(
    'leg_L0_knee_main_loc',  # 타겟 오브젝트
    'leg_L0_low_twist_ctl_aim',  # 소스 오브젝트
    aimVector=[-1, 0, 0],  # aim 벡터
    upVector=[0, 1, 0],   # 업 벡터
    worldUpType="object",  # 월드 업 타입
    worldUpObject="leg_L0_low_twist_null",  # 월드 업 오브젝트
    mo=True
)

# 오른쪽
cmds.aimConstraint(
    'leg_R0_hip_main_loc',  # 타겟 오브젝트
    'leg_R0_up_twist_ctl_aim',  # 소스 오브젝트
    aimVector=[1, 0, 0],  # aim 벡터
    upVector=[0, 1, 0],   # 업 벡터
    worldUpType="object",  # 월드 업 타입
    worldUpObject="leg_R0_up_twist_null",  # 월드 업 오브젝트
    mo=True
)

cmds.aimConstraint(
    'leg_R0_knee_main_loc',  # 타겟 오브젝트
    'leg_R0_low_twist_ctl_aim',  # 소스 오브젝트
    aimVector=[-1, 0, 0],  # aim 벡터
    upVector=[0, 1, 0],   # 업 벡터
    worldUpType="object",  # 월드 업 타입
    worldUpObject="leg_R0_low_twist_null",  # 월드 업 오브젝트
    mo=True
)

cmds.select(cl=1)

## multidivide node 만들어서 손목 돌아갈때 트위스트 0.5 돌아가게 세팅
 
side_list = ['L0', 'R0'] 

# 팔 상박
section = 'arm'        
level = 'up'      
part = 'elbow'
control = 'hand'   

for side in side_list:
    # Utility 노드 생성
    multiply_divide = cmds.shadingNode('multiplyDivide', asUtility=True, n=f'{section}_{side}_{level}_twist_ctl_mul_multiplyDivide')
    blend_colors = cmds.shadingNode('blendColors', asUtility=True, n=f'{section}_{side}_{level}_twist_ctl_mul_blendColors')

    # elbow의 rotateX 연결
    cmds.connectAttr(f'{section}_{side}_{part}_ik_jnt.rotateX', f'{multiply_divide}.input1X', force=True)
    cmds.connectAttr(f'{section}_{side}_{part}_fk_jnt.rotateX', f'{multiply_divide}.input1Y', force=True)

    # multiplyDivide.input2X, input2Y 값 설정
    cmds.setAttr(f'{multiply_divide}.input2X', 0.5)
    cmds.setAttr(f'{multiply_divide}.input2Y', 0.5)

    cmds.connectAttr(f'{multiply_divide}.outputX', f'{blend_colors}.color1R', force=True)

    cmds.connectAttr(f'{multiply_divide}.outputY', f'{blend_colors}.color2R', force=True)

    cmds.connectAttr(f'{control}_{side}_master_ctl.Fk_Ik_switch', f'{blend_colors}.blender', force=True)

    cmds.connectAttr(f'{blend_colors}.outputR', f'{section}_{side}_{level}_twist_ctl_mul.rotateX', force=True)

    cmds.select(cl=1)

# 팔 하박
section = 'arm'        
level = 'low'      
part = 'wrist'
control = 'hand'   

for side in side_list:

    multiply_divide = cmds.shadingNode('multiplyDivide', asUtility=True, n=f'{section}_{side}_{level}_twist_ctl_mul_multiplyDivide')
    blend_colors = cmds.shadingNode('blendColors', asUtility=True, n=f'{section}_{side}_{level}_twist_ctl_mul_blendColors')

    cmds.connectAttr(f'{section}_{side}_{part}_ik_jnt.rotateX', f'{multiply_divide}.input1X', force=True)
    cmds.connectAttr(f'{section}_{side}_{part}_fk_jnt.rotateX', f'{multiply_divide}.input1Y', force=True)

    cmds.setAttr(f'{multiply_divide}.input2X', 0.5)
    cmds.setAttr(f'{multiply_divide}.input2Y', 0.5)

    cmds.connectAttr(f'{multiply_divide}.outputX', f'{blend_colors}.color1R', force=True)

    cmds.connectAttr(f'{multiply_divide}.outputY', f'{blend_colors}.color2R', force=True)

    cmds.connectAttr(f'{control}_{side}_master_ctl.Fk_Ik_switch', f'{blend_colors}.blender', force=True)

    cmds.connectAttr(f'{blend_colors}.outputR', f'{section}_{side}_{level}_twist_ctl_mul.rotateX', force=True)

    cmds.select(cl=1)

side_list = ['L0', 'R0'] 

# 다리 상박
section = 'leg'        
level = 'up'      
part = 'knee'
control = 'foot'   

for side in side_list:

    multiply_divide = cmds.shadingNode('multiplyDivide', asUtility=True, n=f'{section}_{side}_{level}_twist_ctl_mul_multiplyDivide')
    blend_colors = cmds.shadingNode('blendColors', asUtility=True, n=f'{section}_{side}_{level}_twist_ctl_mul_blendColors')

    cmds.connectAttr(f'{section}_{side}_{part}_ik_jnt.rotateX', f'{multiply_divide}.input1X', force=True)
    cmds.connectAttr(f'{section}_{side}_{part}_fk_jnt.rotateX', f'{multiply_divide}.input1Y', force=True)

    cmds.setAttr(f'{multiply_divide}.input2X', 0.5)
    cmds.setAttr(f'{multiply_divide}.input2Y', 0.5)

    cmds.connectAttr(f'{multiply_divide}.outputX', f'{blend_colors}.color1R', force=True)

    cmds.connectAttr(f'{multiply_divide}.outputY', f'{blend_colors}.color2R', force=True)

    cmds.connectAttr(f'{control}_{side}_master_ctl.Fk_Ik_switch', f'{blend_colors}.blender', force=True)

    cmds.connectAttr(f'{blend_colors}.outputR', f'{section}_{side}_{level}_twist_ctl_mul.rotateX', force=True)

    cmds.select(cl=1)

# 다리 하박
section = 'leg'        
level = 'low'      
part = 'foot'
control = 'foot'   

for side in side_list:

    multiply_divide = cmds.shadingNode('multiplyDivide', asUtility=True, n=f'{section}_{side}_{level}_twist_ctl_mul_multiplyDivide')
    blend_colors = cmds.shadingNode('blendColors', asUtility=True, n=f'{section}_{side}_{level}_twist_ctl_mul_blendColors')

    cmds.connectAttr(f'{section}_{side}_{part}_ik_jnt.rotateX', f'{multiply_divide}.input1X', force=True)
    cmds.connectAttr(f'{section}_{side}_{part}_fk_jnt.rotateX', f'{multiply_divide}.input1Y', force=True)

    cmds.setAttr(f'{multiply_divide}.input2X', 0.5)
    cmds.setAttr(f'{multiply_divide}.input2Y', 0.5)

    cmds.connectAttr(f'{multiply_divide}.outputX', f'{blend_colors}.color1R', force=True)

    cmds.connectAttr(f'{multiply_divide}.outputY', f'{blend_colors}.color2R', force=True)

    cmds.connectAttr(f'{control}_{side}_master_ctl.Fk_Ik_switch', f'{blend_colors}.blender', force=True)

    cmds.connectAttr(f'{blend_colors}.outputR', f'{section}_{side}_{level}_twist_ctl_mul.rotateX', force=True)

    cmds.select(cl=1)

## 리본에 바인드한 조인트와 컨트롤러 연걸

def poi_con0_2_L(parent_1, parent_2, parent_3, child_1, child_2, weight_1, weight_2):
    cmds.pointConstraint(parent_1, child_1, mo=False, weight=weight_1)
    cmds.pointConstraint(parent_2, child_1, mo=False, weight=weight_2)
    cmds.pointConstraint(parent_2, child_2, mo=False, weight=weight_1)
    cmds.pointConstraint(parent_3, child_2, mo=False, weight=weight_2)

def poi_con0_2_R(parent_1, parent_2, parent_3, child_1, child_2, weight_1, weight_2):
    cmds.pointConstraint(parent_1, child_1, mo=False, weight=weight_2)
    cmds.pointConstraint(parent_2, child_1, mo=False, weight=weight_1)
    cmds.pointConstraint(parent_2, child_2, mo=False, weight=weight_2)
    cmds.pointConstraint(parent_3, child_2, mo=False, weight=weight_1)

def ori_con0(parent, child, weight):
    cmds.orientConstraint(parent, child, mo=False, weight=weight)

def ori_con1(parent, child, weight):
    return cmds.orientConstraint(parent, child, mo=True, weight=weight)

def par_con1(parent, child, weight):
    return cmds.parentConstraint(parent, child, mo=True, weight=weight)

def par_con0(parent, child, weight):
    return cmds.parentConstraint(parent, child, mo=False, weight=weight)

# point constraint
# 'L0' 또는 'R0'와 같은 정확한 값을 사용하여 각 사이드에 대해 이름을 지정
weights_list = [
    (1, 0),
    (5, 1),
    (2, 1),
    (1, 1),
    (1, 2),
    (1, 5),
    (0, 1)
]

# 사이드가 L0일 때
side = 'L0'
parent_1 = f'arm_{side}_shoulder_main_jnt'
parent_2 = f'arm_{side}_elbow_main_jnt'
parent_3 = f'arm_{side}_wrist_main_jnt'

for i, (weight_1, weight_2) in enumerate(weights_list, start=1):
    poi_con0_2_L(parent_1, parent_2, parent_3, f'arm_{side}_up_folliclejoint{i}_rb_poi', f'arm_{side}_low_folliclejoint{i}_rb_poi', weight_1, weight_2)
    ori_con0(parent_1, f'arm_{side}_up_folliclejoint{i}_rb_poi', 1)
    ori_con0(parent_2, f'arm_{side}_low_folliclejoint{i}_rb_poi', 1)

# 사이드가 R0일 때
side = 'R0'
parent_1 = f'arm_{side}_shoulder_main_jnt'
parent_2 = f'arm_{side}_elbow_main_jnt'
parent_3 = f'arm_{side}_wrist_main_jnt'

for i, (weight_1, weight_2) in enumerate(weights_list, start=1):
    poi_con0_2_R(parent_1, parent_2, parent_3, f'arm_{side}_up_folliclejoint{i}_rb_poi', f'arm_{side}_low_folliclejoint{i}_rb_poi', weight_1, weight_2)
    ori_con0(parent_1, f'arm_{side}_up_folliclejoint{i}_rb_poi', 1)
    ori_con0(parent_2, f'arm_{side}_low_folliclejoint{i}_rb_poi', 1)

# leg 조인트 처리
side = 'L0'
parent_1 = f'leg_{side}_hip_main_jnt'
parent_2 = f'leg_{side}_knee_main_jnt'
parent_3 = f'leg_{side}_foot_main_jnt'

for i, (weight_1, weight_2) in enumerate(weights_list, start=1):
    poi_con0_2_L(parent_1, parent_2, parent_3, f'leg_{side}_up_folliclejoint{i}_rb_poi', f'leg_{side}_low_folliclejoint{i}_rb_poi', weight_1, weight_2)
    ori_con0(parent_1, f'leg_{side}_up_folliclejoint{i}_rb_poi', 1)
    ori_con0(parent_2, f'leg_{side}_low_folliclejoint{i}_rb_poi', 1)

# 사이드가 R0일 때 leg 처리
side = 'R0'
parent_1 = f'leg_{side}_hip_main_jnt'
parent_2 = f'leg_{side}_knee_main_jnt'
parent_3 = f'leg_{side}_foot_main_jnt'

for i, (weight_1, weight_2) in enumerate(weights_list, start=1):
    poi_con0_2_R(parent_1, parent_2, parent_3, f'leg_{side}_up_folliclejoint{i}_rb_poi', f'leg_{side}_low_folliclejoint{i}_rb_poi', weight_1, weight_2)
    ori_con0(parent_1, f'leg_{side}_up_folliclejoint{i}_rb_poi', 1)
    ori_con0(parent_2, f'leg_{side}_low_folliclejoint{i}_rb_poi', 1)

# 마지막 constraint 설정
weights_list = [0, 0, 0, 1, 0, 0, 0]
side_list = ['L0', 'R0']
section_list = ['arm', 'leg']
level_list = ['up', 'low']

for side in side_list:
    for section in section_list:
        for level in level_list:
            for i, weight in enumerate(weights_list, start=1):
                par_con1(f'{section}_{side}_{level}_twist_ctl', f'{section}_{side}_{level}_folliclejoint{i}_rb_par', weight)

## 최종 바인딩 조인트에 parent 연결

cmds.select(cl=1)

side = 'L0'
section = 'arm'
level1 =  'up'
level2 = 'low'
part1 = 'shoulder'
part2 = 'elbow'
part3 = 'wrist'
cmds.parentConstraint(f'{section}_{side}_{level1}_folliclejoint1', f'{section}_{side}_{part1}_bind_jnt', mo=True, weight=1)
cmds.parentConstraint(f'{section}_{side}_{level1}_folliclejoint2', f'{section}_{side}_{level1}_folliclejoint3', f'{section}_{side}_{level1}_folliclejoint4', f'{section}_{side}_twist0_bind_jnt', mo=True, weight=1)
cmds.parentConstraint(f'{section}_{side}_{level1}_folliclejoint4', f'{section}_{side}_{level1}_folliclejoint5', f'{section}_{side}_{level1}_folliclejoint6', f'{section}_{side}_twist1_bind_jnt', mo=True, weight=1)
cmds.parentConstraint(f'{section}_{side}_{level2}_folliclejoint1', f'{section}_{side}_{part2}_bind_jnt', mo=True, weight=1)
cmds.parentConstraint(f'{section}_{side}_{level2}_folliclejoint2', f'{section}_{side}_{level2}_folliclejoint3', f'{section}_{side}_{level2}_folliclejoint4', f'{section}_{side}_twist2_bind_jnt', mo=True, weight=1)
cmds.parentConstraint(f'{section}_{side}_{level2}_folliclejoint4', f'{section}_{side}_{level2}_folliclejoint5', f'{section}_{side}_{level2}_folliclejoint6', f'{section}_{side}_twist3_bind_jnt', mo=True, weight=1)
cmds.parentConstraint(f'{section}_{side}_{part3}_main_jnt', f'{section}_{side}_{part3}_bind_jnt', mo=True, weight=1)
side = 'R0'
cmds.parentConstraint(f'{section}_{side}_{level1}_folliclejoint7', f'{section}_{side}_{part1}_bind_jnt', mo=True, weight=1)
cmds.parentConstraint(f'{section}_{side}_{level1}_folliclejoint6', f'{section}_{side}_{level1}_folliclejoint5', f'{section}_{side}_{level1}_folliclejoint4', f'{section}_{side}_twist0_bind_jnt', mo=True, weight=1)
cmds.parentConstraint(f'{section}_{side}_{level1}_folliclejoint4', f'{section}_{side}_{level1}_folliclejoint3', f'{section}_{side}_{level1}_folliclejoint2', f'{section}_{side}_twist1_bind_jnt', mo=True, weight=1)
cmds.parentConstraint(f'{section}_{side}_{level2}_folliclejoint7', f'{section}_{side}_{part2}_bind_jnt', mo=True, weight=1)
cmds.parentConstraint(f'{section}_{side}_{level2}_folliclejoint6', f'{section}_{side}_{level2}_folliclejoint5', f'{section}_{side}_{level2}_folliclejoint4', f'{section}_{side}_twist2_bind_jnt', mo=True, weight=1)
cmds.parentConstraint(f'{section}_{side}_{level2}_folliclejoint4', f'{section}_{side}_{level2}_folliclejoint3', f'{section}_{side}_{level2}_folliclejoint2', f'{section}_{side}_twist3_bind_jnt', mo=True, weight=1)
cmds.parentConstraint(f'{section}_{side}_{part3}_main_jnt', f'{section}_{side}_{part3}_bind_jnt', mo=True, weight=1)
side = 'L0'
section = 'leg'
part1 = 'hip'
part2 = 'knee'
part3 = 'foot'
cmds.parentConstraint(f'{section}_{side}_{level1}_folliclejoint1', f'{section}_{side}_{part1}_bind_jnt', mo=True, weight=1)
cmds.parentConstraint(f'{section}_{side}_{level1}_folliclejoint2', f'{section}_{side}_{level1}_folliclejoint3', f'{section}_{side}_{level1}_folliclejoint4', f'{section}_{side}_twist0_bind_jnt', mo=True, weight=1)
cmds.parentConstraint(f'{section}_{side}_{level1}_folliclejoint4', f'{section}_{side}_{level1}_folliclejoint5', f'{section}_{side}_{level1}_folliclejoint6', f'{section}_{side}_twist1_bind_jnt', mo=True, weight=1)
cmds.parentConstraint(f'{section}_{side}_{level2}_folliclejoint1', f'{section}_{side}_{part2}_bind_jnt', mo=True, weight=1)
cmds.parentConstraint(f'{section}_{side}_{level2}_folliclejoint2', f'{section}_{side}_{level2}_folliclejoint3', f'{section}_{side}_{level2}_folliclejoint4', f'{section}_{side}_twist2_bind_jnt', mo=True, weight=1)
cmds.parentConstraint(f'{section}_{side}_{level2}_folliclejoint4', f'{section}_{side}_{level2}_folliclejoint5', f'{section}_{side}_{level2}_folliclejoint6', f'{section}_{side}_twist3_bind_jnt', mo=True, weight=1)
cmds.parentConstraint(f'{section}_{side}_{part3}_main_jnt', f'{section}_{side}_{part3}_bind_jnt', mo=True, weight=1)
side = 'R0'
cmds.parentConstraint(f'{section}_{side}_{level1}_folliclejoint7', f'{section}_{side}_{part1}_bind_jnt', mo=True, weight=1)
cmds.parentConstraint(f'{section}_{side}_{level1}_folliclejoint6', f'{section}_{side}_{level1}_folliclejoint5', f'{section}_{side}_{level1}_folliclejoint4', f'{section}_{side}_twist0_bind_jnt', mo=True, weight=1)
cmds.parentConstraint(f'{section}_{side}_{level1}_folliclejoint4', f'{section}_{side}_{level1}_folliclejoint3', f'{section}_{side}_{level1}_folliclejoint2', f'{section}_{side}_twist1_bind_jnt', mo=True, weight=1)
cmds.parentConstraint(f'{section}_{side}_{level2}_folliclejoint7', f'{section}_{side}_{part2}_bind_jnt', mo=True, weight=1)
cmds.parentConstraint(f'{section}_{side}_{level2}_folliclejoint6', f'{section}_{side}_{level2}_folliclejoint5', f'{section}_{side}_{level2}_folliclejoint4', f'{section}_{side}_twist2_bind_jnt', mo=True, weight=1)
cmds.parentConstraint(f'{section}_{side}_{level2}_folliclejoint4', f'{section}_{side}_{level2}_folliclejoint3', f'{section}_{side}_{level2}_folliclejoint2', f'{section}_{side}_twist3_bind_jnt', mo=True, weight=1)
cmds.parentConstraint(f'{section}_{side}_{part3}_main_jnt', f'{section}_{side}_{part3}_bind_jnt', mo=True, weight=1)

## 조인트들과 리본 스키닝 하는 코드

section_list = ['arm', 'leg']
side_list = ['L0', 'R0']
level_list = ['up', 'low']

for section in section_list:
    for side in side_list:
        for level in level_list:
            cmds.select(clear=True)
            cmds.skinCluster(
                f'{section}_{side}_{level}_folliclejoint1_rb',
                f'{section}_{side}_{level}_folliclejoint2_rb',
                f'{section}_{side}_{level}_folliclejoint3_rb',
                f'{section}_{side}_{level}_folliclejoint4_rb',
                f'{section}_{side}_{level}_folliclejoint5_rb',
                f'{section}_{side}_{level}_folliclejoint6_rb',
                f'{section}_{side}_{level}_folliclejoint7_rb',
                f'{section}_{side}_{level}_twist_rib',
                toSelectedBones=True,
                bindMethod=0,
                normalizeWeights=True,
                weightDistribution=0,
                mi=5,
                omi=True,
                dr=4,
                rui=True
                )

## 손폭/팔목 로테이트X 재지정

def create_joint_connections_L0(section, side, part, level):
    """
    주어진 섹션, 방향, 부품 및 레벨을 기준으로 조인트 연결을 생성합니다.
    
    :param section: 섹션 이름 (예: 'arm', 'leg')
    :param side: 방향 (예: 'L0', 'R0')
    :param part: 부품 이름 (예: 'elbow', 'wrist')
    :param level: 레벨 이름 (예: 'up', 'low')
    """
    # 이름 설정
    name = f'{section}_{side}_{part}_main_jnt'
    
    # MultiplyDivide 노드 생성
    multiply_divide0 = cmds.shadingNode('multiplyDivide', asUtility=True, n=f'{name}_multiplyDivide0')
    multiply_divide1 = cmds.shadingNode('multiplyDivide', asUtility=True, n=f'{name}_multiplyDivide1')
    
    # 회전 연결
    for axes in ['X', 'Y', 'Z']:
        cmds.connectAttr(f'{name}.rotateX', f'{multiply_divide0}.input1{axes}', force=True)
        cmds.connectAttr(f'{name}.rotateX', f'{multiply_divide1}.input1{axes}', force=True)
    
    # MultiplyDivide 출력 연결 (사용자 코드대로)
    cmds.connectAttr(f'{multiply_divide0}.outputX', f"{section}_{side}_{level}_folliclejoint1_rb_rot.rotateX", force=True)
    cmds.connectAttr(f'{multiply_divide0}.outputY', f"{section}_{side}_{level}_folliclejoint2_rb_rot.rotateX", force=True)
    cmds.connectAttr(f'{multiply_divide0}.outputZ', f"{section}_{side}_{level}_folliclejoint3_rb_rot.rotateX", force=True)
    cmds.connectAttr(f'{multiply_divide1}.outputX', f"{section}_{side}_{level}_folliclejoint4_rb_rot.rotateX", force=True)
    cmds.connectAttr(f'{multiply_divide1}.outputY', f"{section}_{side}_{level}_folliclejoint5_rb_rot.rotateX", force=True)
    cmds.connectAttr(f'{multiply_divide1}.outputZ', f"{section}_{side}_{level}_folliclejoint6_rb_rot.rotateX", force=True)
    cmds.connectAttr(f'{name}.rotateX', f"{section}_{side}_{level}_folliclejoint7_rb_rot.rotateX", force=True)
    
    # MultiplyDivide 노드 값 설정
    cmds.setAttr(f'{multiply_divide0}.input2X', 0)
    cmds.setAttr(f'{multiply_divide0}.input2Y', 0.16666)
    cmds.setAttr(f'{multiply_divide0}.input2Z', 0.33333)
    cmds.setAttr(f'{multiply_divide1}.input2X', 0.5)
    cmds.setAttr(f'{multiply_divide1}.input2Y', 0.66666)
    cmds.setAttr(f'{multiply_divide1}.input2Z', 0.83333)

cmds.select(cl=True)

# 함수 호출 예제
create_joint_connections_L0('arm', 'L0', 'elbow', 'up')
create_joint_connections_L0('arm', 'L0', 'wrist', 'low')
create_joint_connections_L0('leg', 'L0', 'knee', 'up')
create_joint_connections_L0('leg', 'L0', 'foot', 'low')

def create_joint_connections_R0(section, side, part, level):
    
    name = f'{section}_{side}_{part}_main_jnt'
    
    multiply_divide0 = cmds.shadingNode('multiplyDivide', asUtility=True, n=f'{name}_multiplyDivide0')
    multiply_divide1 = cmds.shadingNode('multiplyDivide', asUtility=True, n=f'{name}_multiplyDivide1')
    
    for axes in ['X', 'Y', 'Z']:
        cmds.connectAttr(f'{name}.rotateX', f'{multiply_divide0}.input1{axes}', force=True)
        cmds.connectAttr(f'{name}.rotateX', f'{multiply_divide1}.input1{axes}', force=True)
    
    cmds.connectAttr(f'{multiply_divide0}.outputX', f"{section}_{side}_{level}_folliclejoint7_rb_rot.rotateX", force=True)
    cmds.connectAttr(f'{multiply_divide0}.outputY', f"{section}_{side}_{level}_folliclejoint6_rb_rot.rotateX", force=True)
    cmds.connectAttr(f'{multiply_divide0}.outputZ', f"{section}_{side}_{level}_folliclejoint5_rb_rot.rotateX", force=True)
    cmds.connectAttr(f'{multiply_divide1}.outputX', f"{section}_{side}_{level}_folliclejoint4_rb_rot.rotateX", force=True)
    cmds.connectAttr(f'{multiply_divide1}.outputY', f"{section}_{side}_{level}_folliclejoint3_rb_rot.rotateX", force=True)
    cmds.connectAttr(f'{multiply_divide1}.outputZ', f"{section}_{side}_{level}_folliclejoint2_rb_rot.rotateX", force=True)
    cmds.connectAttr(f'{name}.rotateX', f"{section}_{side}_{level}_folliclejoint1_rb_rot.rotateX", force=True)
    
    cmds.setAttr(f'{multiply_divide0}.input2X', 0)
    cmds.setAttr(f'{multiply_divide0}.input2Y', 0.16666)
    cmds.setAttr(f'{multiply_divide0}.input2Z', 0.33333)
    cmds.setAttr(f'{multiply_divide1}.input2X', 0.5)
    cmds.setAttr(f'{multiply_divide1}.input2Y', 0.66666)
    cmds.setAttr(f'{multiply_divide1}.input2Z', 0.83333)

cmds.select(cl=True)

create_joint_connections_R0('arm', 'R0', 'elbow', 'up')
create_joint_connections_R0('arm', 'R0', 'wrist', 'low')
create_joint_connections_R0('leg', 'R0', 'knee', 'up')
create_joint_connections_R0('leg', 'R0', 'foot', 'low')

## 밴드 컨트롤러 비저빌리티 설정을 넣을경우 마스터 컨트롤러에 연결해주는 코드

section = 'arm'
part = 'hand'
side_list = ['L0', 'R0']

for side in side_list:
    cmds.connectAttr(f'{part}_{side}_master_ctl.Bend_visibility', f'{section}_{side}_up_twist_ctl.visibility', force=True)
    cmds.connectAttr(f'{part}_{side}_master_ctl.Bend_visibility', f'{section}_{side}_low_twist_ctl.visibility', force=True)

cmds.select(cl=True)

section = 'leg'
part = 'foot'

for side in side_list:
    cmds.connectAttr(f'{part}_{side}_master_ctl.Bend_visibility', f'{section}_{side}_up_twist_ctl.visibility', force=True)
    cmds.connectAttr(f'{part}_{side}_master_ctl.Bend_visibility', f'{section}_{side}_low_twist_ctl.visibility', force=True)

cmds.select(cl=True)

####################################### 작동확인 #######################################