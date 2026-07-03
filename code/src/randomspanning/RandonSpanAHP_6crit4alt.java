/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package randomspanning;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.text.DecimalFormat;
import java.text.NumberFormat;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Random;


/**
 *
 * @author sirajs
 */
public class RandonSpanAHP_6crit4alt {

    Random _rng = new Random();
    String _path = "./";
    /**
     * @param args the command line arguments
     * @throws java.io.IOException
     */
    public static void main(String[] args) throws IOException {
        // TODO code application logic here
        RandonSpanAHP_6crit4alt app = new RandonSpanAHP_6crit4alt();
        
        ExampleBase example1 = (ExampleBase)(new Example_Consistent());
        app.dumpPopulation(example1);
        app.dumpSamples(example1);
        
        ExampleBase example2 = (ExampleBase)(new Example_SaatySchool());
        app.dumpPopulation(example2);
        app.dumpSamples(example2);
    }
    
    public void dumpPopulation(ExampleBase example) throws IOException {
        BufferedWriter fprop;
        PC A_top = example.get_top();
        final int M = example.getPCM(0).getColumnDimension();
        final int N = example.getPCM(1).getColumnDimension();
        
        //* Comment this to resume existing file          
        fprop = new BufferedWriter(
                new FileWriter(_path+example.getName()+"-pop.csv", false));
        fprop.write( "key,set");
        for(int k=0; k<N;k++)fprop.write( ",w"+(1+k) );
        fprop.write( ",key_top");
        for(int k=0; k<M;k++)fprop.write( ",key_"+(1+k) );
        fprop.write( "\n");
        fprop.close();
        /* */
                
        ArrayList<PC> taus_top = doFullSpanning(A_top);
        ArrayList<PC> taus_c1 = doFullSpanning(example.getPCM(1));
        ArrayList<PC> taus_c2 = doFullSpanning(example.getPCM(2));
        ArrayList<PC> taus_c3 = doFullSpanning(example.getPCM(3));
        ArrayList<PC> taus_c4 = doFullSpanning(example.getPCM(4));
        ArrayList<PC> taus_c5 = doFullSpanning(example.getPCM(5));
        ArrayList<PC> taus_c6 = doFullSpanning(example.getPCM(6));

        int progress=0;
        for(PC tau_top : taus_top){
            System.out.print(""+" "+(progress++));
            if(0==progress%10)System.out.println();
            
            for(PC tau_c1: taus_c1){
            for(PC tau_c2: taus_c2){
            for(PC tau_c3: taus_c3){
            for(PC tau_c4: taus_c4){
            for(PC tau_c5: taus_c5){
            for(PC tau_c6: taus_c6){
                double[] w_top = extract(tau_top);
                double[] w_c1 = extract(tau_c1);
                double[] w_c2 = extract(tau_c2);
                double[] w_c3 = extract(tau_c3);
                double[] w_c4 = extract(tau_c4);
                double[] w_c5 = extract(tau_c5);
                double[] w_c6 = extract(tau_c6);

                double[] scores = new double[w_c1.length];
                String str = A_top.hashSpanningTree(tau_top);
                str += ""+example.getPCM(1).hashSpanningTree(tau_c1);
                str += ""+example.getPCM(2).hashSpanningTree(tau_c2);
                str += ""+example.getPCM(3).hashSpanningTree(tau_c3);
                str += ""+example.getPCM(4).hashSpanningTree(tau_c4);
                str += ""+example.getPCM(5).hashSpanningTree(tau_c5);
                str += ""+example.getPCM(6).hashSpanningTree(tau_c6);
                str += ",0";
                for(int j=0; j<scores.length; j++){
                    scores[j] = ( w_c1[j]*w_top[0] 
                                + w_c2[j]*w_top[1] 
                                + w_c3[j]*w_top[2] 
                                + w_c4[j]*w_top[3] 
                                + w_c5[j]*w_top[4] 
                                + w_c6[j]*w_top[5] );
                    str += ","+scores[j];
                }                
                str += ","+A_top.hashSpanningTree(tau_top);
                str += ","+example.getPCM(1).hashSpanningTree(tau_c1);
                str += ","+example.getPCM(2).hashSpanningTree(tau_c2);
                str += ","+example.getPCM(3).hashSpanningTree(tau_c3);
                str += ","+example.getPCM(4).hashSpanningTree(tau_c4);
                str += ","+example.getPCM(5).hashSpanningTree(tau_c5);
                str += ","+example.getPCM(6).hashSpanningTree(tau_c6);
                
                fprop = new BufferedWriter(
                        new FileWriter(_path+example.getName()+"-pop.csv", true));
                fprop.write(str+"\n");
                fprop.close();
            }}}}}}
        }
    }
    
    public void dumpSamples(ExampleBase example) throws IOException {
        BufferedWriter fprop;
        PC A_top = example.get_top();
        final int M = example.getPCM(0).getColumnDimension();
        final int N = example.getPCM(1).getColumnDimension();
        
        //* Comment this to resume existing file          
        fprop = new BufferedWriter(
                new FileWriter(_path+example.getName()+"-samples.csv", false));
        fprop.write( "key,set");
        for(int k=0; k<N;k++)fprop.write( ",w"+(1+k) );
        fprop.write( ",key_top");
        for(int k=0; k<M;k++)fprop.write( ",key_"+(1+k) );
        fprop.write( "\n");
        fprop.close();
        /* */
    
        int nSets=20;
        int nIterations=10000;
        for(int set=0; set<nSets; set++){
            System.out.print(""+" "+(1+set));
            if(0==set%10)System.out.println();
            
            for(int k=0; k<nIterations; k++){
                PC tau_top = doRandomSpanning(A_top);
                PC tau_c1 = doRandomSpanning(example.getPCM(1));
                PC tau_c2 = doRandomSpanning(example.getPCM(2));
                PC tau_c3 = doRandomSpanning(example.getPCM(3));
                PC tau_c4 = doRandomSpanning(example.getPCM(4));
                PC tau_c5 = doRandomSpanning(example.getPCM(5));
                PC tau_c6 = doRandomSpanning(example.getPCM(6));
                double[] w_top = extract(tau_top);
                double[] w_c1 = extract(tau_c1);
                double[] w_c2 = extract(tau_c2);
                double[] w_c3 = extract(tau_c3);
                double[] w_c4 = extract(tau_c4);
                double[] w_c5 = extract(tau_c5);
                double[] w_c6 = extract(tau_c6);

                double[] scores = new double[w_c1.length];
                String str = A_top.hashSpanningTree(tau_top);
                str += ""+example.getPCM(1).hashSpanningTree(tau_c1);
                str += ""+example.getPCM(2).hashSpanningTree(tau_c2);
                str += ""+example.getPCM(3).hashSpanningTree(tau_c3);
                str += ""+example.getPCM(4).hashSpanningTree(tau_c4);
                str += ""+example.getPCM(5).hashSpanningTree(tau_c5);
                str += ""+example.getPCM(6).hashSpanningTree(tau_c6);
                str += ","+(1+set);
                for(int j=0; j<scores.length; j++){
                    scores[j] = ( w_c1[j]*w_top[0] 
                                + w_c2[j]*w_top[1] 
                                + w_c3[j]*w_top[2] 
                                + w_c4[j]*w_top[3] 
                                + w_c5[j]*w_top[4] 
                                + w_c6[j]*w_top[5] );
                    str += ","+scores[j];
                }
                str += ","+A_top.hashSpanningTree(tau_top);
                str += ","+example.getPCM(1).hashSpanningTree(tau_c1);
                str += ","+example.getPCM(2).hashSpanningTree(tau_c2);
                str += ","+example.getPCM(3).hashSpanningTree(tau_c3);
                str += ","+example.getPCM(4).hashSpanningTree(tau_c4);
                str += ","+example.getPCM(5).hashSpanningTree(tau_c5);
                str += ","+example.getPCM(6).hashSpanningTree(tau_c6);
                
                fprop = new BufferedWriter(
                        new FileWriter(_path+example.getName()+"-samples.csv", true));
                fprop.write(str+"\n");
                fprop.close();
            }
        }
    }
    
    
    private ArrayList<PC> doFullSpanning( PC A ){
        HashMap<Integer, Judgment> J = A.Matrix2Map();
        boolean[] V = new boolean[A.n()];
        boolean[] E = new boolean[J.size()];
        for( int i=0; i<E.length; i++ ){E[i]=false;}
        for( int i=0; i<V.length; i++ ){V[i]=false;}
        
        HashMap<String, int[]> vForest= new HashMap<>();
        span(J, vForest, E, V);
        
        // convert hash map to PC list.
        ArrayList<PC> forest = new ArrayList<>();
        Collection<int[]> c = vForest.values();
        Iterator<int[]> e = c.iterator();
        while(e.hasNext() ){
            int[] tree = e.next();
            PC tau = ExampleBase.createPC(A.n());
            for(int k=0; k<tree.length; k++){
                Judgment j = J.get(tree[k]);
                tau.set(j.i, j.j, j.a);
                tau.set(j.j, j.i, 1.0/j.a);
            }
            forest.add(tau);
        }
        return forest;
    }
    
    void span( HashMap<Integer, Judgment> J, HashMap<String, int[]> vForest,
            boolean[] E, boolean[] V ){
        for( int k=0; k<E.length; k++ ){
            if(!E[k]){
                boolean[] vEdges = E.clone();
                boolean[] vNodes = V.clone();

                Judgment a = J.get(k);
                if( vNodes[a.i] && vNodes[a.j] ){ continue; }
                if( !vNodes[a.i] ){ vNodes[a.i]=true; }
                if( !vNodes[a.j] ){ vNodes[a.j]=true; }
                boolean done=true;
                for(int p=0; p<vNodes.length; p++){
                    if(!vNodes[p]){ done = false; }
                }
                vEdges[a.id]=true;

                int count=0;
                for(int p=0; p<vEdges.length; p++){
                    count += (vEdges[p])?1:0;
                }
                if(count!=(vNodes.length-1)){
                    done=false;
                }
                if(done){
                    int[] vE = new int[count];
                    int kk=0;
                    for(int ii=0; ii<vEdges.length; ii++){
                       if(vEdges[ii]){
                           Judgment aa = J.get(ii);
                           vE[kk] = aa.id;
                           kk++;
                       }
                    }
                    Arrays.sort(vE);
                    String key = "";
                    for(int ii=0; ii<vE.length; ii++){
                        final String SEPARATOR = ".";
                        key+= SEPARATOR+(vE[ii]+1);
                    }
                    vForest.put(key, vE);
                }else{
                    span(J, vForest, vEdges, vNodes);
                }
            }
        }
    }

    public PC doRandomSpanning(PC A){
        ArrayList<Integer> vTied = new ArrayList<>();
        ArrayList<Integer> vFree = new ArrayList<>();
        for(int i=0; i<A.n(); i++){
            vFree.add(i);
        }
        PC A_tau = new PC(A.n());
        for( int i=0; i<A_tau.n(); i++ ){
            for( int j=0; j<A_tau.n(); j++ ){
                A_tau.set(i, j, -1);
            }
        }
        for(int iter=0; iter<A.n(); iter++){
            if(vFree.size()>0){
                int idxOneOfFree = _rng.nextInt(vFree.size());
                Integer dstNode = vFree.remove(idxOneOfFree);
                if(vTied.size()>0){
                    for(int k=0; k<50; k++){
                        int idxOneOfTied = _rng.nextInt(vTied.size());
                        Integer srcNode = vTied.get(idxOneOfTied);
                        if(A.get(srcNode, dstNode)>0){
                            A_tau.set(srcNode, dstNode, A.get(srcNode, dstNode));
                            A_tau.set(dstNode, srcNode, A.get(dstNode, srcNode));
                            break;
                        }
                    }
                }
                vTied.add(dstNode);
            }
        }
        return A_tau;
    }


    private double[] extract(PC tau) {
        final int n = tau.getColumnDimension();
        double[] w = new double[n];
        for( int i=0; i<n; i++)w[i]= -1.0; // start with invalid numbers
        w[0] = 1; // set first node as reference
        dfs(tau, w, 0);
        
        return normalize(w); // distributed-mode normalization
    }
    
    // Recursing for depth-first search (dfs)
    private void dfs(PC tau, double[] w, int j){
        final int n = tau.getColumnDimension();
        for(int i=0; i<n; i++){
            if(i!=j){
                double a_ij = tau.get(i,j);
                if(a_ij>0 && w[j]>0 && w[i]<0){
                    w[i] = w[j]*a_ij;
                    dfs(tau, w, i);
                }
            }
        }
    }
    
    public static double[] normalize(double[] w) {
        double ans[] = new double[w.length];
        double sum = 0;
        for (int i = 0; i<w.length; i++) {
            ans[i]=Math.abs(w[i]);
            sum += ans[i];
        }
        if (sum>0){
            for (int i=0; i<ans.length; i++) {
                ans[i] = ans[i]/sum;
            }
        }
        return ans;
    }
    

    public static String asCSV(double[] data) {
        if (data == null) { return ""; }
        String str = "" + data.length + ",1,";
        int j;
        NumberFormat formatter = new DecimalFormat("#.000000000");
        for (j = 0; j < data.length; j++) {
            str += formatter.format(data[j]) + ",";
        }
        str += "EOR";
        return str;
    }
    
}
