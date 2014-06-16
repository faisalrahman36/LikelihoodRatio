#===========================================================================
#
# plot_m.py
#
# Python script to query SWIRE_ES1 mysql database to determine the
# LR the likelihood ratio.
#
#===========================================================================
#
# S. Weston
# AUT University
# March 2013
#===========================================================================

def plot_lr_rel():

    print "\nStarting Plot Likelihood Ratio vs Reliability"

#   Connect to the local database with the atlas uid

    db=_mysql.connect(host=db_host,user=db_user,passwd=db_passwd)

# select from matches the sum of L_i grouped by radio source

    db.query("select lr,reliability,log10(lr) from "+schema+"."+field+"_matches where reliability > 0.0 and reliability < 1.0;" )
          
# store_result() returns the entire result set to the client immediately.
# The other is to use use_result(), which keeps the result set in the server 
#and sends it row-by-row when you fetch.

#r=db.store_result()
# ...or...
    r=db.use_result()

# fetch results, returning char we need float !

    rows=r.fetch_row(maxrows=5000)

# rows is a tuple, convert it to a list

    LR=[]
    REL=[]
    LOG10_LR=[]
 

    for row in rows:
        
        LR.append(float(row[0]))
        REL.append(float(row[1]))
        LOG10_LR.append(float(row[2]))
        
	
#    End of do block

# Close connection to the database
    db.close()

# Now plot Rel vs LR

    print "Plot LR vs Reliability"

    plt.xscale('log')
    plt.plot(LR, REL,'k.')
	
    plot_title='ATLAS ' +field+ ' Reliability vs Likelihood Ratio'
    plt.title(plot_title)
    plt.ylabel('Reliability')
    plt.xlabel('Likelihood Ratio')
    plt.grid(True)
    plt.ylim((-0.1,1.1))
    plot_fname='atlas_' +field+ '_rel_vs_lr.ps'
    fname=output_dir + plot_fname
    plt.savefig(fname,orientation='landscape')
    plt.show()

# Bin Reliability and plot	

#    (hist,bins)=numpy.histogram(f_rows,bins=60,range=[-1.0,5.0])
    (hist,bins)=numpy.histogram(REL,bins=10,range=[0.0,1.0])
    print bins,'\n'
    print hist,'\n'
    width = 1.0*(bins[1]-bins[0])
#    center = (bins[:-1]+bins[1:])/2
    center = 0.5*(bins[1:]+bins[:-1])
    plot_title='ATLAS ' +field+ ' Histogram of the Reliability values'
    plt.title(plot_title)
    plt.yscale('log')
    plt.grid(True)
#    plt.xlim((-0.1,1.1))
    plt.ylabel('N(counterparts)')
    plt.xlabel('Reliability')
#   edgecolor, linestyle, linewidth
#    plt.bar(center, hist, align = 'center',fill=False,edgecolor='0.0', width = width,linewidth=1)
#    plt.plot(center, hist, 'k-')
    common_params = dict(bins=10,
                         range=(0,1))
    common_params['histtype'] = 'step'
    plt.hist(REL,**common_params)
#    pylab.hist(hist, bins=bins, normed=1,histtype='step')
    plot_fname='atlas_' +field+ '_N_vs_rel.ps'
    fname=output_dir + plot_fname
    plt.savefig(fname,orientation='landscape')
    plt.show()
	
# Bin LR and plot

    (hist,bins)=numpy.histogram(LR,bins=100,range=[0.0,1000.0])
    width = 1.0*(bins[1]-bins[0])
    center = 0.5*(bins[:-1]+bins[1:])
    print bins,'\n'
    print hist,'\n'
    plot_title='ATLAS ' +field+ ' Histogram of the Likelihood Ratio values'
    plt.title(plot_title)
    plt.yscale('log')
    plt.xscale('log')
    plt.ylabel('N(counterparts)')
    plt.xlabel('Likelihood Ratio')
#   edgecolor, linestyle, linewidth
#    plt.bar(center, hist, align = 'center',fill=False,edgecolor='0.0', width = width,linewidth=1)
    common_params = dict(bins=100,
                         range=(0,1000))
    common_params['histtype'] = 'step'
    plt.hist(LR,**common_params)
#    plt.plot(center, hist, 'k--', linewidth=1.5)
    plot_fname='atlas_' +field+ '_N_vs_lr.ps'
    fname=output_dir + plot_fname
    plt.savefig(fname,orientation='landscape')
    plt.show()
    
    print "End Plotting\n"


