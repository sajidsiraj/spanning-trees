/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package randomspanning;

import java.util.ArrayList;

import Jama.EigenvalueDecomposition;
import Jama.Matrix;

/**
 *
 * @author sirajs
 */
public class ConsistencyAnalyzer {

    static public double findPerronRoot(PC A) {
        EigenvalueDecomposition ev = A.eig();
        Matrix evd = ev.getD();
        int n = A.getRowDimension();

        int LemdaRow = 0;
        double LemdaMax = evd.get(LemdaRow, LemdaRow);
        for (int i = 0; i < n; i++) {
            double d = evd.get(i, i);
            if (d > LemdaMax) {
                LemdaMax = d;
//                LemdaRow = i;
            }
        }
        return LemdaMax;
    }

    static public double CR(PC A) {
        final double RI[] = {0.00, 0.00, 1.00, 0.58, 0.90, 1.12, 1.24,
            1.32, 1.41, 1.45, 1.51, 1.56, 1.59, 1.60};
        double LemdaMax = findPerronRoot(A);
        int n = A.getRowDimension();
        double CI = Math.abs((LemdaMax - n) / (n - 1));
        double CR = CI;
        if (n >= 2 && n <= RI.length) {
            CR = CI / RI[n];
        }
        return CR;
    }

    static public double CM(PC J) {
    	return CM(J,null);
    }
    static public double CM(PC J, ArrayList<Integer> blamed) {
        int n = J.getRowDimension();
        PC matOut = new PC(Matrix.identity(n,n).getArray());

        double CM = 0.0;
        for (int i = 0; i<n; i++) {
            matOut.set(i, i, 0);
            for (int j=(i+1); j<n; j++) {
                for (int k=0; k<n; k++) {
                    if (i!=k&&j!=k) {
                        double a = J.get(i, j);
                        double c = J.get(j, k);
                        double b = J.get(i, k);
                        if(a>0&&b>0&&c>0){
                            double cm_a = (1 / a) * Math.abs(a - (b / c));
                            double cm_b = (1 / b) * Math.abs(b - (a * c));
                            double cm_c = (1 / c) * Math.abs(c - (b / a));
//                            System.out.print("CM: i="+i+", j="+j+", k="+k);
//                            System.out.println(" => a="+cm_a+", b="+cm_b+", c="+cm_c);

                            double cm = cm_a;
                            if (cm > cm_b) { cm = cm_b; }
                            if (cm > cm_c) { cm = cm_c; }
                            if (cm > CM) { 
                            	CM = cm; 
                            	if(blamed!=null){
                            		blamed.clear();
                            		blamed.add(i);
                            		blamed.add(j);
                            		blamed.add(k);
                            	}
                            }
                        }
                    }
                }
            }
        }
        return CM;
    }

}
