/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package randomspanning;

import java.util.ArrayList;

/**
 *
 * @author sirajs
 */
public class IndirectAnalyzer {
    public static class IndirectJudgments{
            public IndirectJudgments(){}
            public IndirectJudgments(int[] k, double[] a2){
                    _k=k; _a2=a2;
            }
            public int[] _k;
            public double[] _a2;

            //TODO: can this be viewed as optical lens aberration??
//            public double _theta;
//            public double _phi;
    };

    public static IndirectJudgments indirect(PC A, int i, int j){
            IndirectJudgments indirect = new IndirectJudgments();
        ArrayList<Double> vIndirect = new ArrayList<>();
        ArrayList<Integer> vK = new ArrayList<>();
        for(int k=0; k<A.n(); k++){
                double a_ik = A.get(i, k);
                double a_kj = A.get(k, j);
                if(a_ik>0 && a_kj>0 && k!=i && k!=j){
                     vIndirect.add(a_ik*a_kj);
                     vK.add(k);
                }
        }
        indirect._a2 = new double[vIndirect.size()];
        indirect._k = new int[vK.size()];
//        indirect._theta=0;
//        indirect._phi=0;
        for(int k=0; k<indirect._a2.length; k++){
                indirect._a2[k]=vIndirect.get(k);
                indirect._k[k] = vK.get(k);
//                double ln = Math.log(A.get(i,j));
//                double ln2 = Math.log(indirect._a2[k]);
//                indirect._theta+= Math.abs(ln-ln2);
//                indirect._phi+= ((ln*ln2)<0)?1:0;
        }
        if(vIndirect.size()>0){
//                indirect._theta/=vIndirect.size();
//                indirect._phi/=vIndirect.size();
        }
        return indirect;
    }
	
    public static PC congruence( PC P ) {
        int n = P.n();
        double[][] ans = new double[n][n];
        for(int i = 0; i<n; i++){
        for(int j = 0; j<n; j++){
            double cong = 0.0;
            if(i!=j){
                double Aij = P.get(i, j);
                if(Aij>0){
                    double b = Math.log(Aij);
                    for (int k = 0; k<n; k++) {
                        double Aik = P.get(i, k);
                        double Akj = P.get(k, j);
                        if ( (j!=k)&&(k!=i)&&(Aik>0)&&(Akj>0) ){
                            double b2 = Math.log(Aik*Akj);
                            cong += Math.abs( b - b2 );
                        }
                    }
                }
            }
            if(n>2){
                ans[i][j] = ( cong/(n-2) );
            }
        }}
        return new PC(ans);
    }

    public static PC dissonance( PC P ) {
        int n = P.n();
        double[][] ans = new double[n][n];
        for(int i = 0; i<n; i++){
        for(int j = 0; j<n; j++){
            double diss = 0.0;
            if(i!=j){
                double Aij = P.get(i, j);
                if(Aij>0){
                    double b = Math.log(Aij);
                    for (int k = 0; k<n; k++) {
                        double Aik = P.get(i, k);
                        double Akj = P.get(k, j);
                        if ( (j!=k)&&(k!=i)&&(Aik>0)&&(Akj>0) ){
                            double b2 = Math.log(Aik*Akj);
                            diss += (b*b2)<0?1.0:0.0;
                        }
                    }
                }
            }
            if(n>2){
                ans[i][j] = ( diss/(n-2) );
            }
        }}
        return new PC(ans);
    }

    public static double measure(PC P){
        int n = P.getRowDimension();
        double ans=0.0;
        for (int i = 0; i<n; i++) {
        for (int j = 0; j<n; j++) {
            if(i!=j)ans+=P.get(i,j);
        }}
        return ans/(n*(n-1));
    }

}
