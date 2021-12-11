# Starting with defining the network structure
from pgmpy.models import BayesianModel
from pgmpy.factors.discrete import TabularCPD

# Define the model structure (also see the instructions)
cancer_model = BayesianModel([('pen', 'car'),
                              ('car', 'more'),
                              ('car', 'time')])

# now defining the parameters.
cpd_smoke = TabularCPD(variable='pen', variable_card=2,
                       values=[[0.8], [0.2]])
cpd_cancer = TabularCPD(variable='car', variable_card=2,
                        values=[[0.667, 0.15],
                                [0.333, 0.85]],
                        evidence=['pen'],
                        evidence_card=[2])
cpd_xray = TabularCPD(variable='more', variable_card=2,
                      values=[[0.6, 0.7],
                              [0.4, 0.3]],
                      evidence=['car'], evidence_card=[2])
cpd_dysp = TabularCPD(variable='time', variable_card=2,
                      values=[[0.5, 0.25],
                              [0.5, 0.75]],
                      evidence=['car'], evidence_card=[2])

# Associating the parameters with the model structure.
cancer_model.add_cpds(cpd_smoke, cpd_cancer, cpd_xray, cpd_dysp)

# Checking if the cpds are valid for the model.
# print(cancer_model.check_model())

# Check d-separations. This is only meant for those interested. You do not need to understand this to do the project.
# print(cancer_model.is_dconnected('Pollution', 'Smoker'))
# print(cancer_model.is_dconnected('Pollution', 'Smoker', observed=['Cancer']))
# print(cancer_model.local_independencies('Xray'))
# print(cancer_model.get_independencies())

# Print model information
# print(cancer_model.edges())
# print(cancer_model.nodes())
# print(cancer_model.get_cpds())

# Doing exact inference using Variable Elimination
from pgmpy.inference import VariableElimination
cancer_infer = VariableElimination(cancer_model)

# Query  . Below is not working in the new pgmpy build
#print(cancer_infer.query(variables=['Dyspnoea'], evidence={'Cancer': 0})['Dyspnoea'])
#print(cancer_infer.query(variables=['Cancer'], evidence={'Smoker': 0, 'Pollution': 0})['Cancer'])


#Below works in pgmpy version 0.1.12
print(cancer_infer.query(variables=['time'], evidence={'more': 1}, joint=False)['time'])
# print(cancer_infer.query(variables=['time'], evidence={'car': 0}, joint=False)['time'])
# print(cancer_infer.query(variables=['more'], evidence={'Dyspnoea': 1, 'Smoker': 0}, joint=False)['Xray'])
