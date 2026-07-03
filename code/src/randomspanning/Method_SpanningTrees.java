/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package randomspanning;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Arrays;
import java.util.Collection;
import java.util.HashMap;
import java.util.Iterator;
import java.util.logging.Level;
import java.util.logging.Logger;


/**
 *
 * @author sirajs
 */
public class Method_SpanningTrees extends Method {

    boolean _geometric=false;
    boolean _explode=false;
    String _explode_spitfile = "siraj2012east-spit.csv";
    
    public Method_SpanningTrees() {
        super("EAST");
    }

    public Method_SpanningTrees(boolean geometric) {
        super("GMAST");
        _geometric=geometric;
    }

    public Method_SpanningTrees(boolean geometric, boolean explode) {
        super("ST");
        _geometric=geometric;
        _explode=explode;
    }

    @Override
    public Result[] doCalculate(PC A) {
        if (A == null) {
            return null;
        }
        double ct = System.nanoTime();
        _A = A;
        int   n = A.n();

        int m=0;
        J.clear();
        for( int i=0; i<n; i++ ){
            for( int j=i+1; j<n; j++ ){
                int[] x = new int[3];
                x[0]=m; x[1]=i; x[2]=j;
                if(_A.get(i,j)>0){
                    J.put(m,x);
                    m++;
                }
            }
        }

        boolean[] E = new boolean[m];
        boolean[] V = new boolean[n];
        for( int i=0; i<E.length; i++ ){E[i]=false;}
        for( int i=0; i<V.length; i++ ){V[i]=false;}
        vForest.clear();
        span(E, V);

        int i=0;
        final int nW = vForest.size();
        Result[] vSol = new Result[nW];
        Collection<int[]> c = vForest.values();
        Iterator<int[]> e = c.iterator();
        if(_explode){
            BufferedWriter fdata;
            try {
                fdata = new BufferedWriter(new FileWriter(_explode_spitfile, false));
                fdata.close();
            } catch (IOException ex) {
                Logger.getLogger(Method_SpanningTrees.class.getName()).log(Level.SEVERE, null, ex);
            }
        }
        while(e.hasNext() ){
            int[] tree = e.next();
            Result res = new Result();
            res._w = extract(A, tree, n);
            vSol[i] = res;
            i++;
        }

        /////////////////////////////////////////////////////
        // AVERAGE W
        double[] meanW = new double[n];
        for(int j=0; j<n; j++ ){meanW[j]=0;}
        for (Result vSol1 : vSol) {
            double[] sol = vSol1._w;
            for(int j=0; j<n; j++ ){
                meanW[j]+=sol[j];
            }
        }
        for(int j=0; j<n; j++ ){meanW[j]/=vSol.length;}
        /////////////////////////////////////////////////////
        
        /////////////////////////////////////////////////////
        // GEOMETRIC MEAN  (GMAST)
        double[] gmeanW_log = new double[n];
        for(int j=0; j<n; j++ ){gmeanW_log[j]=0;}
        for (Result vSol1 : vSol) {
            double[] sol = vSol1._w;
            for(int j=0; j<n; j++ ){
                gmeanW_log[j]+= Math.log10(sol[j]);
            }
        }
        for(int j=0; j<n; j++ ){ 
            gmeanW_log[j] = gmeanW_log[j]/vSol.length;
        }
        double[] gmeanW = new double[n];
        for(int j=0; j<n; j++ ){
            gmeanW[j]=Math.pow(10, gmeanW_log[j]);
        }
        gmeanW = Result.normalize(gmeanW);
        /////////////////////////////////////////////////////

        /////////////////////////////////////////////////////
        // STANDARD DEVIATION
        double[] stdevW = new double[n];
        for(int j=0; j<n; j++ ){stdevW[j]=0;}
        for (Result vSol1 : vSol) {
            double[] sol = vSol1._w;
            double[] dev = new double[n];
            for(int j=0; j<n; j++ ){
                dev[j]=(meanW[j]-sol[j])*(meanW[j]-sol[j]);
                stdevW[j]+=dev[j];
            }
            double mad=0;
            for(int j=1; j<n; j++ ){ mad+=dev[j]; }
            vSol1._obj = new double[1];
            vSol1._obj[0] = mad/n;
        }
        for(int j=0; j<n; j++ ){
            stdevW[j]/=(vSol.length-1);
        }
        /////////////////////////////////////////////////////

        /////////////////////////////////////////////////////
        // CONSISTENCY MEASURE
        double stdev = 0.0;
        for(int j=0; j<n; j++ ){
            stdev+=stdevW[j];
        }stdev/=n;
        /////////////////////////////////////////////////////

        if(_explode){
            _vW = vSol;
        }else if(_geometric){
            Result[] result = new Result[1];
            Result res2 = new Result();
            res2._w = gmeanW;
            res2._obj= new double[1]; res2._obj[0]= stdev;
            result[0] = res2;
            _vW = result;
        }else{
            Result[] result = new Result[1];
            Result res1 = new Result();
            res1._w = meanW;
            res1._obj= new double[1]; res1._obj[0]= stdev;
            result[0] = res1;            
            _vW = result;
        }
        ct = System.nanoTime()-ct;
        if(_vW!=null){
            for (Result _vW1 : _vW) {
                _vW1._CT = ct/1000.0;
            }
        }
        if(nW<=0){
            _vW = new Result[0];        	
        }
        return _vW;
    }

    HashMap<Integer, int[]> J = new HashMap<>();
    HashMap<String, int[]> vForest= new HashMap<>();

    static int level=0;
    void span( boolean[] E, boolean[] V ){
        level++;
        for( int k=0; k<E.length; k++ ){
            if(!E[k]){
                boolean[] vEdges = E.clone();
                boolean[] vNodes = V.clone();

                int[] a = J.get(k);
                int i=a[1]; int j=a[2];

                if( vNodes[i] && vNodes[j] ){ continue; }
                if( !vNodes[i] ){ vNodes[i]=true; }
                if( !vNodes[j] ){ vNodes[j]=true; }
                boolean done=true;
                for(int p=0; p<vNodes.length; p++){
                    if(!vNodes[p]){ done = false; }
                }
                vEdges[a[0]]=true;

                int count=0;
                for(int p=0; p<vEdges.length; p++){
                    count += (vEdges[p])?1:0;
                }
                if(count!=(vNodes.length-1)){
                    done=false;
                }
                if(done){
                    process(vEdges, count);
                }else{
                    span(vEdges, vNodes);
                }
            }
        }
        level--;
    }

    static final String SEPARATOR = ".";
    private void process(boolean[] vEdges, int nE) {
        int[] vE = new int[nE];
        int k=0;
        for(int i=0; i<vEdges.length; i++){
           if(vEdges[i]){
               int[] a = J.get(i);
               vE[k] = a[0];
               k++;
           }
        }

        Arrays.sort(vE);
        String key = "";
        for(int i=0; i<vE.length; i++){
            key+= SEPARATOR+(vE[i]+1);
        }
        vForest.put(key, vE);
    }

    private double[] extract(PC A, int[] tree, int n) {
        double[] w = new double[n];
        for( int i=0; i<n; i++)w[i]=0;

        w[0]=1;
        boolean rerun=true;
        while(rerun){
            rerun=false;
            for(int k=0; k<tree.length; k++){
                int[] a = J.get(tree[k]);
                int i=a[1]; int j=a[2];
                double x = A.get(i,j);
                if(w[i]>0){
                    w[j]=w[i]/x;
                }else if(w[j]>0){
                    w[i]=w[j]*x;
                }else{
                    rerun=true;
                }
            }
        }

        double[] nw = Result.normalize(w);
//        ///// LOG
        if(_explode){
            BufferedWriter fdata;
            try {
                fdata = new BufferedWriter(new FileWriter(_explode_spitfile, true));
                for(int k=0; k<tree.length; k++){
                    int[] a = J.get(tree[k]);
                    int i=a[1]; int j=a[2];
                    fdata.write("a_{"+(i+1)+""+(j+1)+"}," );
                }
                fdata.write(Result.asCSV(nw)+"\n");
                fdata.close();               
            } catch (IOException ex) {
            }
        }
//        /////////
        return nw;
    }
}