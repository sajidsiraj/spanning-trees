/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package randomspanning;

import java.text.DecimalFormat;
import java.text.NumberFormat;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Random;

/**
 *
 * @author sirajs
 */
public class RandomSpanning {

    Random _rng = new Random();
    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        // TODO code application logic here

        PC A_crit = getSaatySchoolCriteria();
        RandomSpanning app = new RandomSpanning();
        HashMap<String,PC> map = new HashMap<>();
        
        boolean allowDuplicate=true;
        int nIterations=4096;
        for(int k=0; k<nIterations; k++){
            PC tau = app.doRandomSpanning(A_crit);
            String key = app.hashSpanningTree(tau);
            if(allowDuplicate){
                key = ""+k;
            }
            if(!map.containsKey(key)){
                map.put(key, tau);
                double[] w = app.extract(tau);
                System.out.print("-> "+key+",W=,"+asCSV(w)+"\n");
            }else{
                System.out.print("DUPLICATE -> "+key+"\n");
                k--;
            }
        }
    }
    
    public String hashSpanningTree(PC tau){
        String hash="";
        tau.build();
        for( int i=0; i<tau.n(); i++ ){
        for( int j=i+1; j<tau.n(); j++ ){
            if(tau.get(i, j)>0){
                hash+="a"+(i+1)+""+(j+1)+"";
            }
        }}
        return hash;
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
                    int idxOneOfTied = _rng.nextInt(vTied.size());
                    Integer srcNode = vTied.get(idxOneOfTied);
                    A_tau.set(srcNode, dstNode, A.get(srcNode, dstNode));
                }
                vTied.add(dstNode);
            }
        }
        return A_tau;
    }
    
    private double[] extract(PC tau) {
        tau.build();
        double[] w = new double[tau.getColumnDimension()];
        
        boolean[] done = new boolean[w.length];
        for(int k=0; k<w.length; k++){done[k]=false;}   
        
        boolean bFirstTime=true;
        int covered=0;
        while(covered<w.length){
        for(int row=0; row<w.length; row++){
            for(int col=0; col<w.length; col++){
                if(tau.get(col,row)>0){
                    if(bFirstTime){
                        w[row] = 1.0;
                        w[col] = w[row]*tau.get(col,row);
                        bFirstTime=false;
                        done[row]=true;covered++; 
                        done[col]=true;covered++;
                    }
                    else if(done[row] && !done[col]){
                        w[col]=w[row]*tau.get(col,row);
                        done[col]=true;covered++;
                    }else if(!done[row] && done[col]){
                        w[row]=w[col]*tau.get(row,col);
                        done[row]=true;covered++;                        
                    }
                }
            }
        }}
        return normalize(w);
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
    
    public static PC getSaatySchoolCriteria(){
        PC c1 = new PC(6);
        for( int i=0; i<c1.n(); i++ ){
        for( int j=0; j<c1.n(); j++ ){
            c1.set(i, j, -1);
        }}
        c1.set(0, 1, 4);
        c1.set(0, 2, 3);
        c1.set(0, 3, 1);
        c1.set(0, 4, 3);
        c1.set(0, 5, 4);
        
        c1.set(1, 2, 7);
        c1.set(1, 3, 3);
        c1.set(1, 4, 1.0/5);
        c1.set(1, 5, 1);
        
        c1.set(2, 3, 1.0/5);
        c1.set(2, 4, 1.0/5);
        c1.set(2, 5, 1.0/6);
        
        c1.set(3, 4, 1);
        c1.set(3, 5, 1.0/3);
        
        c1.set(4, 5, 3);
        
        c1.build();
        
        return c1;
    }
}
