from flask import Flask, render_template, request, send_file
import pandas as pd
import math
import statistics

app = Flask(__name__)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8001)

@app.route("/", methods=['GET', 'POST'])
def hello_world():
    return render_template('loopy_output.html')

@app.route("/data", methods=['GET', 'POST'])
def data():
    if request.method == 'POST':
        file_1 = request.files['loopy_output_data']
        file_2 = request.files['master_sheet']
        output_data = pd.read_csv(file_1).to_dict()
        master_sheet = pd.read_excel(file_2, engine='openpyxl').to_dict()
        trials = []
        n = 0
        trial_no = 0
        start_trial = 0
        end_trial = 0
        max_dur = 0
        n_i = {'trial_no': [], 'Subject': [], 'Total n': [], 'Total cd': [], 'Total me': [], 'Total lf': [], 'Total ll': [], 'Total md': [], 'Total sd': [], 'Total se': [], 'Total Dur': [], 'Left n': [], 'Left cd': [], 'Left me': [], 'Left lf': [], 'Left ll': [], 'Left md': [], 'Left sd': [], 'Left se': [], 'Right n': [], 'Right cd': [], 'Right me': [], 'Right lf': [], 'Right ll': [], 'Right md': [], 'Right sd': [], 'Right se': [], 'Novel n': [], 'Novel cd': [], 'Novel me': [], 'Novel lf': [], 'Novel ll': [], 'Novel md': [], 'Novel sd': [], 'Novel se': [], 'Sample n': [], 'Sample cd': [], 'Sample me': [], 'Sample lf': [], 'Sample ll': [], 'Sample md': [], 'Sample sd': [], 'Sample se': []}
        while(n<len(output_data['Scoring'])):
            if (output_data['Behaviour'][n]=='Begin Trial'):
                start_trial=n
                max_dur = output_data['Start'][n] + 300
            elif (output_data['Behaviour'][n]=='End Trial'):
                end_trial=n
                d = {'Subject': [], 'Start': [], 'Stop': [], 'Duration': [], 'Behaviour': [], 'Total n': [], 'Total cd': [], 'Total me': [], 'Total lf': [], 'Total ll': [], 'Total md': [], 'Total sd': [], 'Total se': [], 'Total Dur': [], 'Left n': [], 'Left cd': [], 'Left me': [], 'Left lf': [], 'Left ll': [], 'Left md': [], 'Left sd': [], 'Left se': [], 'Right n': [], 'Right cd': [], 'Right me': [], 'Right lf': [], 'Right ll': [], 'Right md': [], 'Right sd': [], 'Right se': []}
                tot_duration = []
                left_duration = []
                right_duration = []
                first_left = True
                left_lf = 0
                left_ll = 0
                first_right = True
                right_lf = 0
                right_ll = 0
                total_ll = 0
                for x in range(start_trial, end_trial+1):
                    if(x!=end_trial and output_data['Start'][x]>max_dur):
                        continue
                    d['Total n'].append(output_data['Stop'][start_trial])
                    d['Total cd'].append(output_data['Stop'][start_trial])
                    d['Total me'].append(output_data['Stop'][start_trial])
                    d['Total lf'].append(output_data['Stop'][start_trial])
                    d['Total ll'].append(output_data['Stop'][start_trial])
                    d['Total md'].append(output_data['Stop'][start_trial])
                    d['Total sd'].append(output_data['Stop'][start_trial])
                    d['Total se'].append(output_data['Stop'][start_trial])
                    d['Total Dur'].append(output_data['Stop'][start_trial])
                    d['Left n'].append(output_data['Stop'][start_trial])
                    d['Left cd'].append(output_data['Stop'][start_trial])
                    d['Left me'].append(output_data['Stop'][start_trial])
                    d['Left lf'].append(output_data['Stop'][start_trial])
                    d['Left ll'].append(output_data['Stop'][start_trial])
                    d['Left md'].append(output_data['Stop'][start_trial])
                    d['Left sd'].append(output_data['Stop'][start_trial])
                    d['Left se'].append(output_data['Stop'][start_trial])
                    d['Right n'].append(output_data['Stop'][start_trial])
                    d['Right cd'].append(output_data['Stop'][start_trial])
                    d['Right me'].append(output_data['Stop'][start_trial])
                    d['Right lf'].append(output_data['Stop'][start_trial])
                    d['Right ll'].append(output_data['Stop'][start_trial])
                    d['Right md'].append(output_data['Stop'][start_trial])
                    d['Right sd'].append(output_data['Stop'][start_trial])
                    d['Right se'].append(output_data['Stop'][start_trial])

                    d['Subject'].append(master_sheet['Subject'][trial_no])
                    d['Start'].append(output_data['Start'][x])
                    d['Stop'].append(output_data['Stop'][x])
                    if (x!=start_trial and x!=end_trial):
                        dur = output_data['Stop'][x] - output_data['Start'][x]
                        d['Duration'].append(dur)
                        tot_duration.append(dur)
                        if (output_data['Behaviour'][x]=='Left Object'):
                            left_duration.append(dur)
                            if first_left:
                                left_lf = x
                                first_left = False
                            left_ll = x   
                        elif (output_data['Behaviour'][x]=='Right Object'):
                            right_duration.append(dur)
                            if first_right:
                                right_lf = x
                                first_right = False
                            right_ll = x   
                    else:
                        d['Duration'].append(output_data['Stop'][start_trial])
                    d['Behaviour'].append(output_data['Behaviour'][x])
                    if x!=end_trial:
                        total_ll = x
                
                d['Total n'][0] = len(tot_duration)
                if len(tot_duration)>0:
                    d['Total cd'][0] = sum(tot_duration)
                    d['Total me'][0] =  sum(tot_duration)/len(tot_duration)
                    d['Total lf'][0] =  output_data['Start'][start_trial+1] - output_data['Start'][start_trial]
                    d['Total ll'][0] =  output_data['Start'][total_ll] - output_data['Start'][start_trial]
                    d['Total md'][0] = statistics.median(tot_duration)
                    d['Total Dur'][0] = output_data['Start'][end_trial] - output_data['Start'][start_trial]
                    n_i['Total cd'].append(sum(tot_duration))
                    n_i['Total me'].append(sum(tot_duration)/len(tot_duration))
                    n_i['Total lf'].append(output_data['Start'][start_trial+1] - output_data['Start'][start_trial])
                    n_i['Total ll'].append(output_data['Start'][total_ll] - output_data['Start'][start_trial])
                    n_i['Total md'].append(statistics.median(tot_duration))
                    n_i['Total Dur'].append(output_data['Start'][end_trial] - output_data['Start'][start_trial])
                else:
                    d['Total cd'][0] = 0
                    d['Total me'][0] = 0
                    d['Total lf'][0] = 0
                    d['Total ll'][0] = 0
                    d['Total md'][0] = 0
                    d['Total Dur'][0] = 0
                    n_i['Total cd'].append(0)
                    n_i['Total me'].append(0)
                    n_i['Total lf'].append(0)
                    n_i['Total ll'].append(0)
                    n_i['Total md'].append(0)
                    n_i['Total Dur'].append(0)
                if len(tot_duration)>1:
                    d['Total sd'][0] = statistics.stdev(tot_duration)
                    d['Total se'][0] = statistics.stdev(tot_duration)/statistics.sqrt(sum(tot_duration))
                    n_i['Total sd'].append(statistics.stdev(tot_duration))
                    n_i['Total se'].append(statistics.stdev(tot_duration)/statistics.sqrt(sum(tot_duration)))
                else:
                    d['Total sd'][0] = '.'
                    d['Total se'][0] = '.'
                    n_i['Total sd'].append('.')
                    n_i['Total se'].append('.')


                d['Left n'][0] = len(left_duration)
                if len(left_duration)>0:
                    d['Left cd'][0] = sum(left_duration)
                    d['Left me'][0] =  sum(left_duration)/len(left_duration)
                    d['Left lf'][0] =  output_data['Start'][left_lf] - output_data['Start'][start_trial]
                    d['Left ll'][0] =  output_data['Start'][left_ll] - output_data['Start'][start_trial]
                    d['Left md'][0] = statistics.median(left_duration)
                    n_i['Left cd'].append(sum(left_duration))
                    n_i['Left me'].append(sum(left_duration)/len(left_duration))
                    n_i['Left lf'].append(output_data['Start'][left_lf] - output_data['Start'][start_trial])
                    n_i['Left ll'].append(output_data['Start'][left_ll] - output_data['Start'][start_trial])
                    n_i['Left md'].append(statistics.median(left_duration))
                else:
                    d['Left cd'][0] = 0
                    d['Left me'][0] = 0
                    d['Left lf'][0] = 0
                    d['Left ll'][0] = 0
                    d['Left md'][0] = 0
                    n_i['Left cd'].append(0)
                    n_i['Left me'].append(0)
                    n_i['Left lf'].append(0)
                    n_i['Left ll'].append(0)
                    n_i['Left md'].append(0)
                if (len(left_duration)>1):
                    d['Left sd'][0] = statistics.stdev(left_duration)
                    d['Left se'][0] = statistics.stdev(left_duration)/statistics.sqrt(sum(left_duration))
                else:
                    d['Left sd'][0] = '.'
                    d['Left se'][0] = '.'

                d['Right n'][0] = len(right_duration)
                if len(right_duration)>0:
                    d['Right cd'][0] = sum(right_duration)
                    d['Right me'][0] =  sum(right_duration)/len(right_duration)
                    d['Right lf'][0] =  output_data['Start'][right_lf] - output_data['Start'][start_trial]
                    d['Right ll'][0] =  output_data['Start'][right_ll] - output_data['Start'][start_trial]
                    d['Right md'][0] = statistics.median(right_duration)
                    n_i['Right cd'].append(sum(right_duration))
                    n_i['Right me'].append(sum(right_duration)/len(right_duration))
                    n_i['Right lf'].append(output_data['Start'][right_lf] - output_data['Start'][start_trial])
                    n_i['Right ll'].append(output_data['Start'][right_ll] - output_data['Start'][start_trial])
                    n_i['Right md'].append(statistics.median(right_duration))
                else:
                    d['Right cd'][0] = 0
                    d['Right me'][0] = 0
                    d['Right lf'][0] = 0
                    d['Right ll'][0] = 0
                    d['Right md'][0] = 0
                    n_i['Right cd'].append(0)
                    n_i['Right me'].append(0)
                    n_i['Right lf'].append(0)
                    n_i['Right ll'].append(0)
                    n_i['Right md'].append(0)
                if (len(right_duration)>1):
                    d['Right sd'][0] = statistics.stdev(right_duration)
                    d['Right se'][0] = statistics.stdev(right_duration)/statistics.sqrt(sum(right_duration))
                else:
                    d['Right sd'][0] = '.'
                    d['Right se'][0] = '.'

                n_i['trial_no'].append(trial_no+1)
                n_i['Subject'].append(master_sheet['Subject'][trial_no])
                n_i['Total n'].append(len(tot_duration))
                n_i['Left n'].append(len(left_duration))
                if(len(left_duration)>1):
                    n_i['Left sd'].append(statistics.stdev(left_duration))
                    n_i['Left se'].append(statistics.stdev(left_duration)/statistics.sqrt(sum(left_duration)))
                else:
                    n_i['Left sd'].append('.')
                    n_i['Left se'].append('.')
                n_i['Right n'].append(len(right_duration))
                if(len(right_duration)>1):
                    n_i['Right sd'].append(statistics.stdev(right_duration))
                    n_i['Right se'].append(statistics.stdev(right_duration)/statistics.sqrt(sum(right_duration)))
                else:
                    n_i['Right sd'].append('.')
                    n_i['Right se'].append('.')
                
                if (master_sheet['Novel Object Name'][trial_no]=='R'):
                    n_i['Sample n'].append(len(left_duration))
                    if len(left_duration)>0:
                        n_i['Sample cd'].append(sum(left_duration))
                        n_i['Sample me'].append(sum(left_duration)/len(left_duration))
                        n_i['Sample lf'].append(output_data['Start'][left_lf] - output_data['Start'][start_trial])
                        n_i['Sample ll'].append(output_data['Start'][left_ll] - output_data['Start'][start_trial])
                        n_i['Sample md'].append(statistics.median(left_duration))
                    else:
                        n_i['Sample cd'].append(0)
                        n_i['Sample me'].append(0)
                        n_i['Sample lf'].append(0)
                        n_i['Sample ll'].append(0)
                        n_i['Sample md'].append(0)
                    if(len(left_duration)>1):
                        n_i['Sample sd'].append(statistics.stdev(left_duration))
                        n_i['Sample se'].append(statistics.stdev(left_duration)/statistics.sqrt(sum(left_duration)))
                    else:
                        n_i['Sample sd'].append('.')
                        n_i['Sample se'].append('.')
                    n_i['Novel n'].append(len(right_duration))
                    if len(right_duration)>0:
                        n_i['Novel cd'].append(sum(right_duration))
                        n_i['Novel me'].append(sum(right_duration)/len(right_duration))
                        n_i['Novel lf'].append(output_data['Start'][right_lf] - output_data['Start'][start_trial])
                        n_i['Novel ll'].append(output_data['Start'][right_ll] - output_data['Start'][start_trial])
                        n_i['Novel md'].append(statistics.median(right_duration))
                    else:
                        n_i['Novel cd'].append(0)
                        n_i['Novel me'].append(0)
                        n_i['Novel lf'].append(0)
                        n_i['Novel ll'].append(0)
                        n_i['Novel md'].append(0)
                    if(len(right_duration)>1):
                        n_i['Novel sd'].append(statistics.stdev(right_duration))
                        n_i['Novel se'].append(statistics.stdev(right_duration)/statistics.sqrt(sum(right_duration)))
                    else:
                        n_i['Novel sd'].append('.')
                        n_i['Novel se'].append('.')
                else:
                    n_i['Novel n'].append(len(left_duration))
                    if len(left_duration)>0:
                        n_i['Novel cd'].append(sum(left_duration))
                        n_i['Novel me'].append(sum(left_duration)/len(left_duration))
                        n_i['Novel lf'].append(output_data['Start'][left_lf] - output_data['Start'][start_trial])
                        n_i['Novel ll'].append(output_data['Start'][left_ll] - output_data['Start'][start_trial])
                        n_i['Novel md'].append(statistics.median(left_duration))
                    else:
                        n_i['Novel cd'].append(0)
                        n_i['Novel me'].append(0)
                        n_i['Novel lf'].append(0)
                        n_i['Novel ll'].append(0)
                        n_i['Novel md'].append(0)
                    if(len(left_duration)>1):
                        n_i['Novel sd'].append(statistics.stdev(left_duration))
                        n_i['Novel se'].append(statistics.stdev(left_duration)/statistics.sqrt(sum(left_duration)))
                    else:
                        n_i['Novel sd'].append('.')
                        n_i['Novel se'].append('.')
                    n_i['Sample n'].append(len(right_duration))
                    if len(right_duration)>0:
                        n_i['Sample cd'].append(sum(right_duration))
                        n_i['Sample me'].append(sum(right_duration)/len(right_duration))
                        n_i['Sample lf'].append(output_data['Start'][right_lf] - output_data['Start'][start_trial])
                        n_i['Sample ll'].append(output_data['Start'][right_ll] - output_data['Start'][start_trial])
                        n_i['Sample md'].append(statistics.median(right_duration))
                    else:
                        n_i['Sample cd'].append(0)
                        n_i['Sample me'].append(0)
                        n_i['Sample lf'].append(0)
                        n_i['Sample ll'].append(0)
                        n_i['Sample md'].append(0)
                    if(len(right_duration)>1):
                        n_i['Sample sd'].append(statistics.stdev(right_duration))
                        n_i['Sample se'].append(statistics.stdev(right_duration)/statistics.sqrt(sum(right_duration)))
                    else:
                        n_i['Sample sd'].append('.')
                        n_i['Sample se'].append('.')

                df = pd.DataFrame(data=d)
                trials.append(df)
                trial_no += 1
            n+=1
        
        for key, value in n_i.items():
            print(key)
            print(len(value))
        
        with pd.ExcelWriter('output.xlsx') as writer:
            for t in range(len(trials)):
                s = "Trial " + str(t+1)
                trials[t].to_excel(writer, sheet_name=s)
            n_f = pd.DataFrame(data=n_i)
            n_f.to_excel(writer, sheet_name='Loopy SAS Nested Index Model', index=False)
            

        return send_file('output.xlsx', as_attachment=True)





