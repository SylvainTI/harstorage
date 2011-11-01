from harstorage.lib.MongoHandler import MongoDB

import logging

from pylons import request, tmpl_context as c

from harstorage.lib.base import BaseController, render

log = logging.getLogger(__name__)

class SuperposedController(BaseController):
    def create(self):
        # MongoDB handler
        md_handler = MongoDB()
        
        # List of labels
        c.labels    = list()
        for label in md_handler.collection.distinct('label'):
            c.labels.append(label)
        
        return render('./create.html')
    
    def dates(self):
        # Label
        label = request.GET['label']

        # MongoDB handler
        md_handler = MongoDB()
        
        dates = str()

        for document in md_handler.collection.find({'label':label}).sort("timestamp",1):
            dates += document['timestamp'] + ';'
            
        return dates[:-1]
            
    def display(self):
        # 5 Arrays for timeline chart
        lbl_points      = str()
        time_points     = str()
        size_points     = str()
        req_points      = str()
        score_points    = str()

        # Initial row count
        c.rowcount = 0
        
        # Summary table canvas
        c.metrics_table = list()
        for index in range(6):
            c.metrics_table.append(list())
        
        # Iteration
        for index in range( len(request.POST) /3 ):
            # Parameters
            label       = request.POST[ 'step_'+str(index+1)+'_label' ]
            start_ts    = request.POST[ 'step_'+str(index+1)+'_start_ts' ]
            end_ts      = request.POST[ 'step_'+str(index+1)+'_end_ts' ]
            
            # Average stats
            time, size, req, score = self.get_avg( label,start_ts,end_ts )
            
            # Ordered labels
            id = str(index + 1)
            if index <9: id = '0' + id
            
            # Data for table
            c.metrics_table[0].append( label    )
            c.metrics_table[1].append( score    )
            c.metrics_table[2].append( size     )
            c.metrics_table[3].append( req      ) 
            c.metrics_table[4].append( time     )
            
            c.rowcount += 1

            label = id + " - " + label

            lbl_points      += str(label)+"#"
            time_points     += str(time)+"#"
            size_points     += str(size)+"#"
            req_points      += str(req)+"#"
            score_points    += str(score)+"#"

        c.points = lbl_points[:-1]+";"\
                    +time_points[:-1]+";"\
                    +size_points[:-1]+";"\
                    +req_points[:-1]+";"\
                    +score_points[:-1]

        return render('./display.html')
        
    def get_avg(self,label,start_ts,end_ts):
        # MongoDB handler
        md_handler = MongoDB()
        
        avg_size    = 0
        avg_time    = 0
        avg_req     = 0
        avg_score   = 0
        count       = md_handler.collection.find({'label':label,"timestamp" : {"$gte" : start_ts, "$lte" : end_ts} }).count()

        for document in md_handler.collection.find({'label':label,"timestamp" : {"$gte" : start_ts, "$lte" : end_ts} }):
            avg_size    += document["total_size"]
            avg_time    += document["full_load_time"]
            avg_req     += document["requests"]
            avg_score   += document['ps_scores']['Total Score']
            
        avg_size    /= count
        avg_time    /= count
        avg_req     /= count
        avg_score   /= count
        
        return avg_time, avg_size, avg_req, avg_score