#------------------------------------------------------------------
# Heading
#------------------------------------------------------------------
#
wipe
model basic -ndm 3 -ndf 6
#
#
#------------------------------------------------------------------
# Nodes
#------------------------------------------------------------------
#
node 1 0.500 3.500 0.000
node 2 4.500 1.000 0.000
node 3 2.000 4.000 0.000
node 4 0.000 2.000 0.000
node 5 4.500 4.000 0.000
node 6 5.000 2.500 0.000
node 7 1.500 4.000 0.000
node 8 3.000 4.000 0.000
node 9 1.500 3.500 0.000
node 10 4.000 4.500 0.000
node 11 1.000 2.500 0.000
node 12 0.500 1.500 0.000
node 13 0.500 2.500 0.000
node 14 5.000 3.000 0.000
node 15 5.000 0.500 0.000
node 16 1.500 2.000 0.000
node 17 0.500 4.000 0.000
node 18 1.500 1.500 0.000
node 19 3.500 4.000 0.000
node 20 2.000 0.500 0.000
node 21 1.000 0.500 0.000
node 22 1.500 4.500 0.000
node 23 2.500 1.500 0.000
node 24 4.500 5.000 0.000
node 25 0.500 0.500 0.000
node 26 5.000 1.000 0.000
node 27 1.500 0.000 0.000
node 28 0.500 2.000 0.000
node 29 4.500 3.500 0.000
node 30 2.500 4.000 0.000
node 31 3.500 1.500 0.000
node 32 2.000 2.500 0.000
node 33 3.000 0.500 0.000
node 34 2.500 3.500 0.000
node 35 3.500 4.500 0.000
node 36 2.000 1.500 0.000
node 37 5.000 4.000 0.000
node 38 1.500 5.000 0.000
node 39 0.500 5.000 0.000
node 40 0.000 4.000 0.000
node 41 2.500 0.500 0.000
node 42 0.500 0.000 0.000
node 43 4.000 2.500 0.000
node 44 4.500 1.500 0.000
node 45 3.500 0.000 0.000
node 46 3.500 3.500 0.000
node 47 1.000 3.000 0.000
node 48 0.000 2.500 0.000
node 49 3.000 2.500 0.000
node 50 4.500 2.500 0.000
node 51 2.000 3.500 0.000
node 52 5.000 2.000 0.000
node 53 1.500 3.000 0.000
node 54 0.500 3.000 0.000
node 55 2.500 2.500 0.000
node 56 3.500 5.000 0.000
node 57 2.500 5.000 0.000
node 58 4.000 0.500 0.000
node 59 3.500 2.000 0.000
node 60 2.500 0.000 0.000
node 61 1.000 1.000 0.000
node 62 5.000 3.500 0.000
node 63 0.000 0.500 0.000
node 64 1.500 2.500 0.000
node 65 4.000 3.500 0.000
node 66 4.500 0.500 0.000
node 67 1.000 3.500 0.000
node 68 1.500 1.000 0.000
node 69 0.500 1.000 0.000
node 70 0.000 3.500 0.000
node 71 4.000 5.000 0.000
node 72 2.500 2.000 0.000
node 73 2.000 4.500 0.000
node 74 1.000 4.500 0.000
node 75 5.000 1.500 0.000
node 76 3.000 1.000 0.000
node 77 1.500 0.500 0.000
node 78 4.000 1.500 0.000
node 79 1.000 1.500 0.000
node 80 0.000 1.500 0.000
node 81 3.500 1.000 0.000
node 82 2.500 1.000 0.000
node 83 4.000 3.000 0.000
node 84 1.000 2.000 0.000
node 85 2.000 1.000 0.000
node 86 1.000 5.000 0.000
node 87 3.000 3.000 0.000
node 88 3.000 4.500 0.000
node 89 4.000 4.000 0.000
node 90 3.500 0.500 0.000
node 91 3.000 1.500 0.000
node 92 3.500 3.000 0.000
node 93 2.500 3.000 0.000
node 94 4.000 1.000 0.000
node 95 4.500 2.000 0.000
node 96 1.000 0.000 0.000
node 97 2.000 3.000 0.000
node 98 5.000 4.500 0.000
node 99 3.000 5.000 0.000
node 100 4.000 2.000 0.000
node 101 3.500 2.500 0.000
node 102 2.000 0.000 0.000
node 103 0.500 4.500 0.000
node 104 3.000 3.500 0.000
node 105 4.500 0.000 0.000
node 106 2.000 5.000 0.000
node 107 3.000 0.000 0.000
node 108 0.000 3.000 0.000
node 109 0.000 4.500 0.000
node 110 4.000 0.000 0.000
node 111 4.500 4.500 0.000
node 112 4.500 3.000 0.000
node 113 2.000 2.000 0.000
node 114 2.500 4.500 0.000
node 115 1.000 4.000 0.000
node 116 3.000 2.000 0.000
node 117 0.000 1.000 0.000
#
#
#
#------------------------------------------------------------------
# Boundary conditions
#------------------------------------------------------------------
#
# disp_left
#----------
#
fix 4 1 1 1 0 0 0
fix 6 1 1 1 0 0 0
fix 14 1 1 1 0 0 0
fix 15 1 1 1 0 0 0
fix 24 1 1 1 0 0 0
fix 26 1 1 1 0 0 0
fix 27 1 1 1 0 0 0
fix 37 1 1 1 0 0 0
fix 38 1 1 1 0 0 0
fix 39 1 1 1 0 0 0
fix 40 1 1 1 0 0 0
fix 42 1 1 1 0 0 0
fix 45 1 1 1 0 0 0
fix 48 1 1 1 0 0 0
fix 52 1 1 1 0 0 0
fix 56 1 1 1 0 0 0
fix 57 1 1 1 0 0 0
fix 60 1 1 1 0 0 0
fix 62 1 1 1 0 0 0
fix 63 1 1 1 0 0 0
fix 70 1 1 1 0 0 0
fix 71 1 1 1 0 0 0
fix 75 1 1 1 0 0 0
fix 80 1 1 1 0 0 0
fix 86 1 1 1 0 0 0
fix 96 1 1 1 0 0 0
fix 98 1 1 1 0 0 0
fix 99 1 1 1 0 0 0
fix 102 1 1 1 0 0 0
fix 105 1 1 1 0 0 0
fix 106 1 1 1 0 0 0
fix 107 1 1 1 0 0 0
fix 108 1 1 1 0 0 0
fix 109 1 1 1 0 0 0
fix 110 1 1 1 0 0 0
fix 117 1 1 1 0 0 0
#
#
#
#------------------------------------------------------------------
# Materials
#------------------------------------------------------------------
#
# mat_elastic
#------------
#
uniaxialMaterial Elastic 1 20000000000
nDMaterial ElasticIsotropic 1001 20000000000 0.3 1500
#
#
#
#------------------------------------------------------------------
# Elements
#------------------------------------------------------------------
#
# ep
#---
#
geomTransf Corotational 1 0 -1 0
element elasticBeamColumn 1 92 46 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 1
#
geomTransf Corotational 2 0 -1 0
element elasticBeamColumn 2 92 83 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 2
#
geomTransf Corotational 3 0 -1 0
element elasticBeamColumn 3 82 76 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 3
#
geomTransf Corotational 4 0 -1 0
element elasticBeamColumn 4 82 23 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 4
#
geomTransf Corotational 5 0 -1 0
element elasticBeamColumn 5 47 53 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 5
#
geomTransf Corotational 6 0 -1 0
element elasticBeamColumn 6 47 67 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 6
#
geomTransf Corotational 7 0 -1 0
element elasticBeamColumn 7 77 20 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 7
#
geomTransf Corotational 8 0 -1 0
element elasticBeamColumn 8 77 68 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 8
#
geomTransf Corotational 9 0 -1 0
element elasticBeamColumn 9 67 115 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 9
#
geomTransf Corotational 10 0 -1 0
element elasticBeamColumn 10 67 9 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 10
#
geomTransf Corotational 11 0 -1 0
element elasticBeamColumn 11 17 115 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 11
#
geomTransf Corotational 12 0 -1 0
element elasticBeamColumn 12 17 103 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 12
#
geomTransf Corotational 13 0 -1 0
element elasticBeamColumn 13 27 77 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 13
#
geomTransf Corotational 14 0 -1 0
element elasticBeamColumn 14 97 51 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 14
#
geomTransf Corotational 15 0 -1 0
element elasticBeamColumn 15 97 93 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 15
#
geomTransf Corotational 16 0 -1 0
element elasticBeamColumn 16 87 104 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 16
#
geomTransf Corotational 17 0 -1 0
element elasticBeamColumn 17 87 92 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 17
#
geomTransf Corotational 18 0 -1 0
element elasticBeamColumn 18 60 41 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 18
#
geomTransf Corotational 19 0 -1 0
element elasticBeamColumn 19 50 112 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 19
#
geomTransf Corotational 20 0 -1 0
element elasticBeamColumn 20 50 6 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 20
#
geomTransf Corotational 21 0 -1 0
element elasticBeamColumn 21 80 12 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 21
#
geomTransf Corotational 22 0 -1 0
element elasticBeamColumn 22 70 1 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 22
#
geomTransf Corotational 23 0 -1 0
element elasticBeamColumn 23 20 41 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 23
#
geomTransf Corotational 24 0 -1 0
element elasticBeamColumn 24 20 85 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 24
#
geomTransf Corotational 25 0 -1 0
element elasticBeamColumn 25 40 17 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 25
#
geomTransf Corotational 26 0 -1 0
element elasticBeamColumn 26 30 114 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 26
#
geomTransf Corotational 27 0 -1 0
element elasticBeamColumn 27 30 8 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 27
#
geomTransf Corotational 28 0 -1 0
element elasticBeamColumn 28 100 43 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 28
#
geomTransf Corotational 29 0 -1 0
element elasticBeamColumn 29 100 95 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 29
#
geomTransf Corotational 30 0 -1 0
element elasticBeamColumn 30 90 81 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 30
#
geomTransf Corotational 31 0 -1 0
element elasticBeamColumn 31 90 58 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 31
#
geomTransf Corotational 32 0 -1 0
element elasticBeamColumn 32 53 9 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 32
#
geomTransf Corotational 33 0 -1 0
element elasticBeamColumn 33 53 97 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 33
#
geomTransf Corotational 34 0 -1 0
element elasticBeamColumn 34 43 83 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 34
#
geomTransf Corotational 35 0 -1 0
element elasticBeamColumn 35 43 50 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 35
#
geomTransf Corotational 36 0 -1 0
element elasticBeamColumn 36 73 114 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 36
#
geomTransf Corotational 37 0 -1 0
element elasticBeamColumn 37 73 106 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 37
#
geomTransf Corotational 38 0 -1 0
element elasticBeamColumn 38 63 25 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 38
#
geomTransf Corotational 39 0 -1 0
element elasticBeamColumn 39 13 54 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 39
#
geomTransf Corotational 40 0 -1 0
element elasticBeamColumn 40 13 11 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 40
#
geomTransf Corotational 41 0 -1 0
element elasticBeamColumn 41 33 76 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 41
#
geomTransf Corotational 42 0 -1 0
element elasticBeamColumn 42 33 90 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 42
#
geomTransf Corotational 43 0 -1 0
element elasticBeamColumn 43 23 72 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 43
#
geomTransf Corotational 44 0 -1 0
element elasticBeamColumn 44 23 91 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 44
#
geomTransf Corotational 45 0 -1 0
element elasticBeamColumn 45 5 37 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 45
#
geomTransf Corotational 46 0 -1 0
element elasticBeamColumn 46 5 111 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 46
#
geomTransf Corotational 47 0 -1 0
element elasticBeamColumn 47 8 88 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 47
#
geomTransf Corotational 48 0 -1 0
element elasticBeamColumn 48 8 19 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 48
#
geomTransf Corotational 49 0 -1 0
element elasticBeamColumn 49 7 22 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 49
#
geomTransf Corotational 50 0 -1 0
element elasticBeamColumn 50 7 3 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 50
#
geomTransf Corotational 51 0 -1 0
element elasticBeamColumn 51 2 44 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 51
#
geomTransf Corotational 52 0 -1 0
element elasticBeamColumn 52 2 26 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 52
#
geomTransf Corotational 53 0 -1 0
element elasticBeamColumn 53 83 65 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 53
#
geomTransf Corotational 54 0 -1 0
element elasticBeamColumn 54 83 112 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 54
#
geomTransf Corotational 55 0 -1 0
element elasticBeamColumn 55 1 67 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 55
#
geomTransf Corotational 56 0 -1 0
element elasticBeamColumn 56 1 17 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 56
#
geomTransf Corotational 57 0 -1 0
element elasticBeamColumn 57 4 28 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 57
#
geomTransf Corotational 58 0 -1 0
element elasticBeamColumn 58 3 30 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 58
#
geomTransf Corotational 59 0 -1 0
element elasticBeamColumn 59 3 73 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 59
#
geomTransf Corotational 60 0 -1 0
element elasticBeamColumn 60 93 87 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 60
#
geomTransf Corotational 61 0 -1 0
element elasticBeamColumn 61 93 34 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 61
#
geomTransf Corotational 62 0 -1 0
element elasticBeamColumn 62 10 71 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 62
#
geomTransf Corotational 63 0 -1 0
element elasticBeamColumn 63 10 111 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 63
#
geomTransf Corotational 64 0 -1 0
element elasticBeamColumn 64 9 51 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 64
#
geomTransf Corotational 65 0 -1 0
element elasticBeamColumn 65 9 7 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 65
#
geomTransf Corotational 66 0 -1 0
element elasticBeamColumn 66 58 94 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 66
#
geomTransf Corotational 67 0 -1 0
element elasticBeamColumn 67 58 66 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 67
#
geomTransf Corotational 68 0 -1 0
element elasticBeamColumn 68 48 13 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 68
#
geomTransf Corotational 69 0 -1 0
element elasticBeamColumn 69 78 100 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 69
#
geomTransf Corotational 70 0 -1 0
element elasticBeamColumn 70 78 44 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 70
#
geomTransf Corotational 71 0 -1 0
element elasticBeamColumn 71 68 85 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 71
#
geomTransf Corotational 72 0 -1 0
element elasticBeamColumn 72 68 18 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 72
#
geomTransf Corotational 73 0 -1 0
element elasticBeamColumn 73 18 16 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 73
#
geomTransf Corotational 74 0 -1 0
element elasticBeamColumn 74 18 36 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 74
#
geomTransf Corotational 75 0 -1 0
element elasticBeamColumn 75 28 13 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 75
#
geomTransf Corotational 76 0 -1 0
element elasticBeamColumn 76 28 84 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 76
#
geomTransf Corotational 77 0 -1 0
element elasticBeamColumn 77 88 99 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 77
#
geomTransf Corotational 78 0 -1 0
element elasticBeamColumn 78 88 35 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 78
#
geomTransf Corotational 79 0 -1 0
element elasticBeamColumn 79 54 47 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 79
#
geomTransf Corotational 80 0 -1 0
element elasticBeamColumn 80 54 1 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 80
#
geomTransf Corotational 81 0 -1 0
element elasticBeamColumn 81 44 75 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 81
#
geomTransf Corotational 82 0 -1 0
element elasticBeamColumn 82 44 95 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 82
#
geomTransf Corotational 83 0 -1 0
element elasticBeamColumn 83 74 22 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 83
#
geomTransf Corotational 84 0 -1 0
element elasticBeamColumn 84 74 86 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 84
#
geomTransf Corotational 85 0 -1 0
element elasticBeamColumn 85 64 32 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 85
#
geomTransf Corotational 86 0 -1 0
element elasticBeamColumn 86 64 53 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 86
#
geomTransf Corotational 87 0 -1 0
element elasticBeamColumn 87 34 104 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 87
#
geomTransf Corotational 88 0 -1 0
element elasticBeamColumn 88 34 30 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 88
#
geomTransf Corotational 89 0 -1 0
element elasticBeamColumn 89 94 78 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 89
#
geomTransf Corotational 90 0 -1 0
element elasticBeamColumn 90 94 2 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 90
#
geomTransf Corotational 91 0 -1 0
element elasticBeamColumn 91 84 16 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 91
#
geomTransf Corotational 92 0 -1 0
element elasticBeamColumn 92 84 11 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 92
#
geomTransf Corotational 93 0 -1 0
element elasticBeamColumn 93 59 100 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 93
#
geomTransf Corotational 94 0 -1 0
element elasticBeamColumn 94 59 101 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 94
#
geomTransf Corotational 95 0 -1 0
element elasticBeamColumn 95 49 87 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 95
#
geomTransf Corotational 96 0 -1 0
element elasticBeamColumn 96 49 101 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 96
#
geomTransf Corotational 97 0 -1 0
element elasticBeamColumn 97 79 84 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 97
#
geomTransf Corotational 98 0 -1 0
element elasticBeamColumn 98 79 18 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 98
#
geomTransf Corotational 99 0 -1 0
element elasticBeamColumn 99 69 61 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 99
#
geomTransf Corotational 100 0 -1 0
element elasticBeamColumn 100 69 12 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 100
#
geomTransf Corotational 101 0 -1 0
element elasticBeamColumn 101 19 35 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 101
#
geomTransf Corotational 102 0 -1 0
element elasticBeamColumn 102 19 89 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 102
#
geomTransf Corotational 103 0 -1 0
element elasticBeamColumn 103 29 5 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 103
#
geomTransf Corotational 104 0 -1 0
element elasticBeamColumn 104 29 62 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 104
#
geomTransf Corotational 105 0 -1 0
element elasticBeamColumn 105 89 5 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 105
#
geomTransf Corotational 106 0 -1 0
element elasticBeamColumn 106 89 10 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 106
#
geomTransf Corotational 107 0 -1 0
element elasticBeamColumn 107 105 66 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 107
#
geomTransf Corotational 108 0 -1 0
element elasticBeamColumn 108 107 33 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 108
#
geomTransf Corotational 109 0 -1 0
element elasticBeamColumn 109 108 54 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 109
#
geomTransf Corotational 110 0 -1 0
element elasticBeamColumn 110 101 43 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 110
#
geomTransf Corotational 111 0 -1 0
element elasticBeamColumn 111 101 92 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 111
#
geomTransf Corotational 112 0 -1 0
element elasticBeamColumn 112 102 20 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 112
#
geomTransf Corotational 113 0 -1 0
element elasticBeamColumn 113 103 74 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 113
#
geomTransf Corotational 114 0 -1 0
element elasticBeamColumn 114 103 39 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 114
#
geomTransf Corotational 115 0 -1 0
element elasticBeamColumn 115 104 46 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 115
#
geomTransf Corotational 116 0 -1 0
element elasticBeamColumn 116 104 8 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 116
#
geomTransf Corotational 117 0 -1 0
element elasticBeamColumn 117 109 103 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 117
#
geomTransf Corotational 118 0 -1 0
element elasticBeamColumn 118 110 58 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 118
#
geomTransf Corotational 119 0 -1 0
element elasticBeamColumn 119 55 93 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 119
#
geomTransf Corotational 120 0 -1 0
element elasticBeamColumn 120 55 49 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 120
#
geomTransf Corotational 121 0 -1 0
element elasticBeamColumn 121 45 90 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 121
#
geomTransf Corotational 122 0 -1 0
element elasticBeamColumn 122 65 29 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 122
#
geomTransf Corotational 123 0 -1 0
element elasticBeamColumn 123 65 89 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 123
#
geomTransf Corotational 124 0 -1 0
element elasticBeamColumn 124 35 10 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 124
#
geomTransf Corotational 125 0 -1 0
element elasticBeamColumn 125 35 56 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 125
#
geomTransf Corotational 126 0 -1 0
element elasticBeamColumn 126 25 21 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 126
#
geomTransf Corotational 127 0 -1 0
element elasticBeamColumn 127 25 69 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 127
#
geomTransf Corotational 128 0 -1 0
element elasticBeamColumn 128 95 52 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 128
#
geomTransf Corotational 129 0 -1 0
element elasticBeamColumn 129 95 50 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 129
#
geomTransf Corotational 130 0 -1 0
element elasticBeamColumn 130 85 82 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 130
#
geomTransf Corotational 131 0 -1 0
element elasticBeamColumn 131 85 36 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 131
#
geomTransf Corotational 132 0 -1 0
element elasticBeamColumn 132 115 7 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 132
#
geomTransf Corotational 133 0 -1 0
element elasticBeamColumn 133 115 74 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 133
#
geomTransf Corotational 134 0 -1 0
element elasticBeamColumn 134 116 59 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 134
#
geomTransf Corotational 135 0 -1 0
element elasticBeamColumn 135 116 49 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 135
#
geomTransf Corotational 136 0 -1 0
element elasticBeamColumn 136 117 69 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 136
#
geomTransf Corotational 137 0 -1 0
element elasticBeamColumn 137 111 24 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 137
#
geomTransf Corotational 138 0 -1 0
element elasticBeamColumn 138 111 98 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 138
#
geomTransf Corotational 139 0 -1 0
element elasticBeamColumn 139 51 34 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 139
#
geomTransf Corotational 140 0 -1 0
element elasticBeamColumn 140 51 3 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 140
#
geomTransf Corotational 141 0 -1 0
element elasticBeamColumn 141 41 82 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 141
#
geomTransf Corotational 142 0 -1 0
element elasticBeamColumn 142 41 33 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 142
#
geomTransf Corotational 143 0 -1 0
element elasticBeamColumn 143 61 79 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 143
#
geomTransf Corotational 144 0 -1 0
element elasticBeamColumn 144 61 68 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 144
#
geomTransf Corotational 145 0 -1 0
element elasticBeamColumn 145 11 47 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 145
#
geomTransf Corotational 146 0 -1 0
element elasticBeamColumn 146 11 64 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 146
#
geomTransf Corotational 147 0 -1 0
element elasticBeamColumn 147 112 29 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 147
#
geomTransf Corotational 148 0 -1 0
element elasticBeamColumn 148 112 14 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 148
#
geomTransf Corotational 149 0 -1 0
element elasticBeamColumn 149 31 59 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 149
#
geomTransf Corotational 150 0 -1 0
element elasticBeamColumn 150 31 78 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 150
#
geomTransf Corotational 151 0 -1 0
element elasticBeamColumn 151 21 77 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 151
#
geomTransf Corotational 152 0 -1 0
element elasticBeamColumn 152 21 61 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 152
#
geomTransf Corotational 153 0 -1 0
element elasticBeamColumn 153 113 32 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 153
#
geomTransf Corotational 154 0 -1 0
element elasticBeamColumn 154 113 72 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 154
#
geomTransf Corotational 155 0 -1 0
element elasticBeamColumn 155 114 88 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 155
#
geomTransf Corotational 156 0 -1 0
element elasticBeamColumn 156 114 57 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 156
#
geomTransf Corotational 157 0 -1 0
element elasticBeamColumn 157 91 31 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 157
#
geomTransf Corotational 158 0 -1 0
element elasticBeamColumn 158 91 116 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 158
#
geomTransf Corotational 159 0 -1 0
element elasticBeamColumn 159 81 31 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 159
#
geomTransf Corotational 160 0 -1 0
element elasticBeamColumn 160 81 94 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 160
#
geomTransf Corotational 161 0 -1 0
element elasticBeamColumn 161 46 65 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 161
#
geomTransf Corotational 162 0 -1 0
element elasticBeamColumn 162 46 19 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 162
#
geomTransf Corotational 163 0 -1 0
element elasticBeamColumn 163 76 81 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 163
#
geomTransf Corotational 164 0 -1 0
element elasticBeamColumn 164 76 91 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 164
#
geomTransf Corotational 165 0 -1 0
element elasticBeamColumn 165 66 15 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 165
#
geomTransf Corotational 166 0 -1 0
element elasticBeamColumn 166 66 2 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 166
#
geomTransf Corotational 167 0 -1 0
element elasticBeamColumn 167 16 113 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 167
#
geomTransf Corotational 168 0 -1 0
element elasticBeamColumn 168 16 64 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 168
#
geomTransf Corotational 169 0 -1 0
element elasticBeamColumn 169 36 23 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 169
#
geomTransf Corotational 170 0 -1 0
element elasticBeamColumn 170 36 113 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 170
#
geomTransf Corotational 171 0 -1 0
element elasticBeamColumn 171 96 21 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 171
#
geomTransf Corotational 172 0 -1 0
element elasticBeamColumn 172 42 25 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 172
#
geomTransf Corotational 173 0 -1 0
element elasticBeamColumn 173 72 116 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 173
#
geomTransf Corotational 174 0 -1 0
element elasticBeamColumn 174 72 55 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 174
#
geomTransf Corotational 175 0 -1 0
element elasticBeamColumn 175 12 28 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 175
#
geomTransf Corotational 176 0 -1 0
element elasticBeamColumn 176 12 79 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 176
#
geomTransf Corotational 177 0 -1 0
element elasticBeamColumn 177 32 55 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 177
#
geomTransf Corotational 178 0 -1 0
element elasticBeamColumn 178 32 97 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 178
#
geomTransf Corotational 179 0 -1 0
element elasticBeamColumn 179 22 38 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 179
#
geomTransf Corotational 180 0 -1 0
element elasticBeamColumn 180 22 73 0.007853981633974483 20000000000 7692307692.307692 9.817477042468105e-06 4.9087385212340526e-06 4.9087385212340526e-06 180
#
#
#
#------------------------------------------------------------------
# Steps
#------------------------------------------------------------------
#
# step_load
#----------
#
timeSeries Constant 1 -factor 1.0
pattern Plain 1 1 -fact 1 {
#
# load_weights
#-------------
#