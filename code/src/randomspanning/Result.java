/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package randomspanning;

import java.text.DecimalFormat;
import java.text.NumberFormat;

public class Result{
        public String 			_method;
        public double			_NV;
        public double			_TD;
        public double			_TD2;
        public double			_CT;
        
        public double[]                  _w;
        public double[]                  _obj;
        
        
    	public static int sizeForW(PC _A) {
    		// [ Method, W ]
    		return 1+_A.n();
    	}
    	public static int sizeForObj(PC _A) {
    		// [ Method, NV, TD, TD2, CT ]
    		return 5;
    	}

    	// returns [ Method, NV, TD, TD2 ]
    	public Object prop(int column) {
    		Object res = null;
    		switch(column){
    		case 0:
    			res = _method; 
    			break;    			
    		case 1:
    			res = _NV;
    			break;
    		case 2:
    			res = _TD;
    			break;
    		case 3:
    			res = _TD2;
    			break;
    		case 4:
    			res = _CT;
    			break;
    		}
    		return res;
    	}
    	// returns [ W_1, W_2, ..., W_n ]
    	public Object data(int column) {
    		double[] w = _w;
    		if(column<=0){
    			return _method;
    		}
    		if(column<=w.length){
    			return w[column-1];
    		}
    		return null;
    	}
        
    public double[] normalize() {
        return normalize(_w);
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